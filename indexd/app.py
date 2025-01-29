import os
import sys

import cdislogging
import ddtrace
import flask

from indexd.urls.blueprint import blueprint as index_urls_blueprint

from .alias.blueprint import blueprint as indexd_alias_blueprint
from .blueprint import blueprint as cross_blueprint
from .bulk.blueprint import blueprint as indexd_bulk_blueprint
from .index.blueprint import blueprint as indexd_index_blueprint


def app_init(app, settings=None):
    app.logger.addHandler(cdislogging.get_stream_handler())
    # TODO: When indexd is used by gdcapi (as dev dep during tests),
    # ddtrace patches graphql because of patch_all(). To prevent that
    # we explicitly excluded. At any rate, graphql is NOT used by
    # indexd so it's safe to disable it.
    ddtrace.patch_all(graphql=False)
    if not settings:
        from .default_settings import settings
    app.config.update(settings["config"])
    app.auth = settings["auth"]
    app.register_blueprint(indexd_bulk_blueprint)
    app.register_blueprint(indexd_index_blueprint)
    app.register_blueprint(indexd_alias_blueprint)
    app.register_blueprint(cross_blueprint)
    app.register_blueprint(index_urls_blueprint, url_prefix="/_query/urls")


def get_app():
    app = flask.Flask("indexd")

    if "INDEXD_SETTINGS" in os.environ:
        sys.path.append(os.environ["INDEXD_SETTINGS"])

    settings = None
    try:
        from local_settings import settings
    except ImportError:
        pass

    app_init(app, settings)

    return app
