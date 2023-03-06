import os

from .alias.drivers.alchemy import SQLAlchemyAliasDriver
from .auth.drivers.alchemy import SQLAlchemyAuthDriver
from .index.drivers.alchemy import SQLAlchemyIndexDriver

CONFIG = {}

CONFIG["JSONIFY_PRETTYPRINT_REGULAR"] = False
AUTO_MIGRATE = True
SQLALCHEMY_VERBOSE = os.getenv("INDEXD_VERBOSE", "").lower() in ["1", "yes", "true"]
PG_HOST = os.getenv("PG_INDEXD_HOST", "localhost")
PG_USER = os.getenv("PG_INDEXD_USER", "test")
PG_PASS = os.getenv("PG_INDEXD_PASS", "test")
PG_DBNAME = os.getenv("PG_INDEXD_DBNAME", "indexd_test")
PG_URL = f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}/{PG_DBNAME}"

CONFIG["INDEX"] = {
    "driver": SQLAlchemyIndexDriver(
        PG_URL,
        auto_migrate=AUTO_MIGRATE,
        echo=SQLALCHEMY_VERBOSE,
        index_config={
            "DEFAULT_PREFIX": "testprefix:",
            "ADD_PREFIX_ALIAS": True,
            "PREPEND_PREFIX": True,
        },
    ),
}

CONFIG["ALIAS"] = {
    "driver": SQLAlchemyAliasDriver(
        PG_URL, auto_migrate=AUTO_MIGRATE, echo=SQLALCHEMY_VERBOSE
    ),
}

AUTH = SQLAlchemyAuthDriver(PG_URL)

settings = {"config": CONFIG, "auth": AUTH}
