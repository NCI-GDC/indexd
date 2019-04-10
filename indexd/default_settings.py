import os

from .alias.drivers.alchemy import SQLAlchemyAliasDriver
from .auth.drivers.alchemy import SQLAlchemyAuthDriver
from .index.drivers.alchemy import SQLAlchemyIndexDriver

CONFIG = {}

CONFIG['JSONIFY_PRETTYPRINT_REGULAR'] = False
AUTO_MIGRATE = True
SQLALCHEMY_VERBOSE = (
    os.getenv('INDEXD_VERBOSE', '').lower() in ['1', 'yes', 'true']
)
PG_URL = 'postgres://test:test@localhost/indexd_test'

CONFIG['INDEX'] = {
    'driver': SQLAlchemyIndexDriver(
        PG_URL, auto_migrate=AUTO_MIGRATE, echo=SQLALCHEMY_VERBOSE,
        index_config={
            'DEFAULT_PREFIX': 'testprefix:',
            'ADD_PREFIX_ALIAS': True,
            'PREPEND_PREFIX': True,
        }
    ),
}

CONFIG['ALIAS'] = {
    'driver': SQLAlchemyAliasDriver(
        PG_URL, auto_migrate=AUTO_MIGRATE, echo=SQLALCHEMY_VERBOSE),
}

CONFIG['DIST'] = [
    {
        'name': 'Other IndexD',
        'host': 'https://indexd.example.io/index/',
        'hints': ['.*ROCKS.*'],
        'type': 'indexd',
    },
    {
        'name': 'DX DOI',
        'host': 'https://doi.org/',
        'hints': ['10\..*'],
        'type': 'doi',
    },
    {
        'name': 'DOS System',
        'host': 'https://example.com/api/ga4gh/dos/v1/',
        'hints': [],
        'type': 'dos',
    },
]

AUTH = SQLAlchemyAuthDriver(PG_URL)

settings = {'config': CONFIG, 'auth': AUTH}
