import flask

from indexd.alias.errors import NoRecordFound as AliasNoRecordFound
from indexd.errors import AuthError, UserError
from indexd.index.errors import NoRecordFound as IndexNoRecordFound

blueprint = flask.Blueprint("cross", __name__)

blueprint.config = dict()
blueprint.index_driver = None
blueprint.alias_driver = None
blueprint.dist = []


@blueprint.route("/alias/<path:alias>", methods=["GET"])
def get_alias(alias):
    """
    Return alias associated information.
    """
    info = blueprint.alias_driver.get(alias)

    start = 0
    limit = 100

    size = info["size"]
    hashes = info["hashes"]

    urls = blueprint.index_driver.get_urls(
        size=size,
        hashes=hashes,
        start=start,
        limit=limit,
    )

    info.update(
        {
            "urls": urls,
            "start": start,
            "limit": limit,
        }
    )

    return flask.jsonify(info), 200


@blueprint.route("/<path:record>", methods=["GET"])
def get_record(record):
    """
    Returns a record from the local ids, alias, or global resolvers.
    """

    try:
        ret = blueprint.index_driver.get(record)
    except IndexNoRecordFound:
        try:
            ret = blueprint.index_driver.get_by_alias(record)
        except IndexNoRecordFound:
            try:
                ret = blueprint.alias_driver.get(record)
            except AliasNoRecordFound:
                raise IndexNoRecordFound("no record found")

    return flask.jsonify(ret), 200


@blueprint.errorhandler(UserError)
def handle_user_error(err):
    return flask.jsonify(error=str(err)), 400


@blueprint.errorhandler(AuthError)
def handle_auth_error(err):
    return flask.jsonify(error=str(err)), 403


@blueprint.errorhandler(AliasNoRecordFound)
def handle_no_record_error(err):
    return flask.jsonify(error=str(err)), 404


@blueprint.errorhandler(IndexNoRecordFound)
def handle_no_record_error(err):
    return flask.jsonify(error=str(err)), 404


@blueprint.record
def get_config(setup_state):
    index_config = setup_state.app.config["INDEX"]
    alias_config = setup_state.app.config["ALIAS"]
    blueprint.index_driver = index_config["driver"]
    blueprint.alias_driver = alias_config["driver"]
    if "DIST" in setup_state.app.config:
        blueprint.dist = setup_state.app.config["DIST"]
