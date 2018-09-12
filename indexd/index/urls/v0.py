import json
import logging

from flask import Blueprint, jsonify, Response

from indexd.errors import UserError
from indexd.index import request_args_to_params
from indexd.index.drivers.query.urls import AlchemyURLsQueryDriver


logger = logging.getLogger("index.urls.blueprint")
urls = Blueprint("urls", __name__)

urls.driver = None  # type: AlchemyURLsQueryDriver


@urls.route("/q", methods=["GET"])
@request_args_to_params
def query(exclude=None, include=None, version=True, fields=None, limit=100, offset=0, **kwargs):
    """ Queries indexes based on URLs
    Args:
        exclude (str): only include documents (did) with urls that does not match this pattern
        include (str): only include documents (did) with a url matching this pattern
        version (str): return only records with version number
        fields (str): comma separated list of fields to return, if not specified return all fields
        limit (str): max results to return
        offset (str): where to start the next query from
    Returns:
        flask.Response: json list of matching entries
            `
                [
                    {"did": "AAAA-BB", "rev": "1ADs" "urls": ["s3://some-randomly-awesome-url"]},
                    {"did": "AAAA-CC", "rev": "2Nsf", "urls": ["s3://another-randomly-awesome-url"]}
                ]
            `
    """

    return jsonify([dict(did="AAAAA", urls=["sss", "ddd"]), dict(did="AAAAA", urls=["sss", "ddd"])]), 200


@urls.route("/metadata/q")
@request_args_to_params
def query_metadata(key, value, url=None, version=False, fields=None, limit="100", offset="0", **kwargs):
    """ Queries indexes by URLs metadata key and value
    Args:
        key (str): metadata key
        value (str): metadata value for key
        url (str): full url or pattern for limit to
        fields (str): comma separated list of fields to return, if not specified return all fields
        version (str): filter only records with a version number
        limit (str): max results to return
        offset (str): where to start the next query from
    """
    records = urls.driver.get_metadata_by_key(key, value, url=url,
                                              only_versioned=version and version.lower() in ["true", "t", "yes", "y"],
                                              offset=int(offset), limit=int(limit))
    records = [dict(did=x[0], urls=[x[1]], rev=x[2]) for x in records]
    return Response(json.dumps(records, indent=2, separators=(', ', ': ')), 200, mimetype="application/json")


@urls.errorhandler(UserError)
def handle_unhealthy_check(err):
    return err.message, 404


@urls.record
def pre_config(state):
    driver = state.app.config["INDEX"]["driver"]
    urls.driver = AlchemyURLsQueryDriver(driver)