import logging
import re
from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector
import sys


FORMAT = '[%(asctime)s][%(name)10s][%(levelname)7s] %(message)s'


def hint_match(record, hints):
    for hint in hints:
        if re.match(hint, record):
            return True
    return False


def try_drop_test_data(
        database='indexd_test', root_user='postgres', host='localhost'):

    # Using an engine that connects to the `postgres` database allows us to
    # create a new database.
    engine = create_engine("postgres://{user}@{host}/postgres".format(
        user=root_user, host=host))

    conn = engine.connect()
    conn.execute("commit")

    try:
        create_stmt = 'DROP DATABASE "{database}"'.format(database=database)
        conn.execute(create_stmt)
    except Exception as e:
        logging.warn("Unable to drop test data: %s", e)

    conn.close()
    engine.dispose()


def setup_database(
        user='test', password='test', database='indexd_test',
        root_user='postgres', host='localhost', no_drop=False, no_user=False):
    """Setup the user and database"""

    if not no_drop:
        try_drop_test_data(database)

    # Create an engine connecting to the `postgres` database allows us to
    # create a new database from there.
    engine = create_engine("postgres://{user}@{host}/postgres".format(
        user=root_user, host=host))
    conn = engine.connect()
    conn.execute("commit")

    create_stmt = 'CREATE DATABASE "{database}"'.format(database=database)
    try:
        conn.execute(create_stmt)
    except Exception:
        logging.warn('Unable to create database')

    if not no_user:
        try:
            user_stmt = "CREATE USER {user} WITH PASSWORD '{password}'".format(
                user=user, password=password)
            conn.execute(user_stmt)

            perm_stmt = 'GRANT ALL PRIVILEGES ON DATABASE {database} to {password}'\
                        ''.format(database=database, password=password)
            conn.execute(perm_stmt)
            conn.execute("commit")
        except Exception as e:
            logging.warn("Unable to add user: %s", e)
    conn.close()


def create_tables(host, user, password, database):
    """
    create tables
    """
    engine = create_engine("postgres://{user}:{pwd}@{host}/{db}".format(
        user=user, host=host, pwd=password, db=database))
    conn = engine.connect()

    create_index_record_stm = "CREATE TABLE index_record (\
        did VARCHAR NOT NULL, rev VARCHAR, form VARCHAR, size BIGINT, PRIMARY KEY (did) )"
    create_record_hash_stm = "CREATE TABLE index_record_hash (\
        did VARCHAR NOT NULL, hash_type VARCHAR NOT NULL, hash_value VARCHAR, \
        PRIMARY KEY (did, hash_type), FOREIGN KEY(did) REFERENCES index_record (did))"
    create_record_url_stm = "CREATE TABLE index_record_url( \
        did VARCHAR NOT NULL, url VARCHAR NOT NULL, PRIMARY KEY (did, url),\
        FOREIGN KEY(did) REFERENCES index_record (did) )"
    create_index_schema_version_stm = "CREATE TABLE index_schema_version (\
        version INT)"
    try:
        conn.execute(create_index_record_stm)
        conn.execute(create_record_hash_stm)
        conn.execute(create_record_url_stm)
        conn.execute(create_index_schema_version_stm)
    except Exception:
        logging.warn('Unable to create table')
    conn.close()


def check_engine_for_migrate(engine):
    """
    check if a db engine support database migration

    Args:
        engine (sqlalchemy.engine.base.Engine): a sqlalchemy engine

    Return:
        bool: whether the engine support migration
    """
    return engine.dialect.supports_alter


def init_schema_version(driver, model, version):
    """
    initialize schema table with a initialized singleton of version

    Args:
        driver (object): an alias or index driver instance
        model (sqlalchemy.ext.declarative.api.Base): the version table model

    Return:
        version (int): current version number in database
    """
    with driver.session as s:
        schema_version = s.query(model).first()
        if not schema_version:
            schema_version = model(version=version)
            s.add(schema_version)
        version = schema_version.version
    return version


def migrate_database(driver, migrate_functions, current_schema_version, model):
    """
    migrate current database to match the schema version provided in
    current schema

    Args:
        driver (object): an alias or index driver instance
        migrate_functions (list): a list of migration functions
        curent_schema_version (int): version of current schema in code
        model (sqlalchemy.ext.declarative.api.Base): the version table model

    Return:
        None
    """
    db_schema_version = init_schema_version(driver, model, 0)

    need_migrate = (current_schema_version - db_schema_version) > 0

    if not check_engine_for_migrate(driver.engine) and need_migrate:
        driver.logger.error(
            'Engine {} does not support alter, skip migration'.format(
                driver.engine.dialect.name))
        return
    for f in migrate_functions[
            db_schema_version:current_schema_version]:
        with driver.session as s:
            schema_version = s.query(model).first()
            schema_version.version += 1
            driver.logger.debug('migrating {} schema to {}'.format(
                driver.__class__.__name__,
                schema_version.version))

            f(engine=driver.engine, session=s)
            s.add(schema_version)
            driver.logger.debug('finished migration for version {}'.format(
                schema_version.version))


def is_empty_database(driver):
    """
    check if the database is empty or not
    Args:
        driver (object): an alias or index driver instance

    Returns:
        Boolean
    """
    table_list = Inspector.from_engine(driver.engine).get_table_names()

    return len(table_list) == 0


def get_stream_handler():
    """Return a stdout stream handler
    All logs will write to stdout.
    Return:
        logging.StreamHandler: pre-formatted file handler
    """

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(FORMAT))

    return handler

def get_file_handler(file_name):
    """Return a file handler
    Args:
        file_name (string): name of file to write logs to
    Return:
        logging.FileHandler: pre-formatted stream handler
    """

    handler = logging.FileHandler(file_name)
    handler.setFormatter(logging.Formatter(FORMAT))

    return handler

def get_logger(logger_name, file_name=None, log_level=None):
    """Return an opinionated basic logger named `name` that logs to stdout
    If you leave the log level argument as None and the logger was not
    previously instantiated, the level will be set to NOTSET. If the logger
    was previously instantiated, the level will be left alone.
    If the level is NOTSET, then ancestor loggers are traversed and searched
    for a log_level and handler. See python docs.
    If you change the log level to something other than debug (or notset) then it will not
    display log statements below that level (see example and chart below for details).
    Ideally this should be handled by your application's command line args.
    eg:
    ```
    log = get_logger('hi', log_level='info')
    log.debug('hello world') # <- this will not display
    ```
    Args:
        logger_name (string): name of the logger
        file_name (string): if present, will write logs to file as well
        log_level (string): level of logging for this logger. string so you
                            don't have to import logging in the application
    Return:
        logging.Logger: pre-formatted logger object
    """

    log_levels = {                  # sorted level
        'notset': logging.NOTSET,   # 00
        'debug': logging.DEBUG,     # 10
        'info': logging.INFO,       # 20
        'warning': logging.WARNING, # 30
        'warn': logging.WARNING,    # 30
        'error': logging.ERROR,     # 40
    }

    logger = logging.getLogger(logger_name)

    if log_level:
        if log_level not in log_levels:
            error_message = 'Invalid log_level parameter: {}\n\n' \
                            'Valid options: debug, info, warning, ' \
                            'warn, error'.format(log_level)
            raise Exception(error_message)

        logger.setLevel(log_levels[log_level])
    # Else, NOTSET is Python default.

    logger.propagate = logger.level == logging.NOTSET

    if logger.level != logging.NOTSET and not logger.handlers:
        logger.addHandler(get_stream_handler())

        if file_name:
            logger.addHandler(get_file_handler(file_name))
    # Else if at least one log handler exists that means it has been
    # instantiated with the same name before. Do not keep creating handlers
    # or your logs will be very messy.
    if logger.level == logging.NOTSET:
        # Delete handlers in case level was set back to NOTSET
        # after being set to something else
        del logger.handlers[:]

    return logger
