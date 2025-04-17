from importlib.metadata import distribution

import logstick

LOG_CFG = logstick.configure_logging(
    namespace=__name__,
    disable_existing_loggers=False,
    extra_namespaces=["gunicorn.access", "gunicorn.error", "werkzeug"],
)
__distribution = distribution(__name__)
VERSION = __distribution.version
