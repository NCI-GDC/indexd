from typing import cast

import sqlalchemy
import sqlalchemy_utils
from sqlalchemy import engine, orm

Base = orm.declarative_base()


class SQLAlchemyDriverBase:
    """
    SQLAlchemy implementation of index driver.
    """

    def __init__(self, conn, **config):
        """
        Initialize the SQLAlchemy database driver.
        """
        self.engine = cast(engine.Engine, sqlalchemy.create_engine(conn, **config))
        if not sqlalchemy_utils.database_exists(self.engine.url):
            sqlalchemy_utils.create_database(self.engine.url)

    def dispose(self):
        self.engine.dispose()
