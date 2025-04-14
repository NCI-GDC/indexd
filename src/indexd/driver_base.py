import sqlalchemy
from sqlalchemy_utils import create_database, database_exists

Base = sqlalchemy.orm.declarative_base()


class SQLAlchemyDriverBase:
    """
    SQLAlchemy implementation of index driver.
    """

    def __init__(self, conn, **config):
        """
        Initialize the SQLAlchemy database driver.
        """
        engine = sqlalchemy.create_engine(conn, **config)
        if not database_exists(engine.url):
            create_database(engine.url)
        self.engine = engine

    def dispose(self):
        self.engine.dispose()
