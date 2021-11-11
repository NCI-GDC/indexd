from indexd import get_app
from elasticapm.contrib.flask import ElasticAPM
import os
os.environ['INDEXD_SETTINGS'] = '/var/www/indexd/'
application = get_app()

application.config['ELASTIC_APM'] = {
    # Set the required service name. Allowed characters:
    # a-z, A-Z, 0-9, -, _, and space
    'SERVICE_NAME': 'indexd',

    # Use if APM Server requires a secret token
    'SECRET_TOKEN': '',

    # Set the custom APM Server URL (default: http://localhost:8200)
    'SERVER_URL': 'http://elastic-apm.service.consul:8200',

    # Set the service environment
    'ENVIRONMENT': '',

    'NO_PROXY': '*',
}

apm = ElasticAPM(application)
