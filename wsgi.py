from indexd import get_app
import os
import pathlib

file = pathlib.Path("/var/www/indexd/newrelic.ini")
if file.exists():
    import newrelic.agent

    newrelic.agent.initialize("/var/www/indexd/newrelic.ini")

os.environ['INDEXD_SETTINGS'] = '/var/www/indexd/'
application = get_app()
