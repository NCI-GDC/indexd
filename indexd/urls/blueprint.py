import json

from flask import Blueprint, Response, request
from flask.json import jsonify

from indexd.errors import UserError
from indexd.index.drivers.query.urls import AlchemyURLsQueryDriver


blueprint = Blueprint("urls", __name__)


@blueprint.route("/q", methods=["GET"])
def query():
    """ Queries indexes based on URLs
    Params:
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

    record_list = blueprint.driver.query_urls(**request.args.to_dict())

    fields = request.args.get("fields", "did,urls")
    fields_dict = requested_fields(fields)

    results = []
    for record in record_list:
        c_response = {}
        if fields_dict.get("did"):
            c_response["did"] = record[0]
        if fields_dict.get("urls"):
            c_response["urls"] = record[1].split(",") if record[1] else []
        results.append(c_response)

    return Response(json.dumps(results, indent=2, separators=(', ', ': ')), 200, mimetype="application/json")


@blueprint.route("/metadata/q")
def query_metadata():
    """ Queries indexes by URLs metadata key and value
    Params:
        key (str): metadata key
        value (str): metadata value for key
        url (str): full url or pattern for limit to
        fields (str): comma separated list of fields to return, if not specified return all fields
        version (str): filter only records with a version number
        limit (str): max results to return
        offset (str): where to start the next query from
    """

    record_list = blueprint.driver.query_metadata_by_key(**request.args.to_dict())
    fields = request.args.get("fields", "did,urls,rev")
    fields_dict = requested_fields(fields)

    results = []
    for record in record_list:
        c_response = {}
        if fields_dict.get("did"):
            c_response["did"] = record[0]
        if fields_dict.get("urls"):
            c_response["urls"] = [record[1]]
        if fields_dict.get("rev"):
            c_response["rev"] = record[2]
        results.append(c_response)

    return Response(json.dumps(results, indent=2, separators=(', ', ': ')), 200, mimetype="application/json")


@blueprint.record
def pre_config(state):
    driver = state.app.config["INDEX"]["driver"]
    blueprint.logger = state.app.logger
    blueprint.driver = AlchemyURLsQueryDriver(driver)


@blueprint.errorhandler(UserError)
def handle_user_error(err):
    return jsonify(error=str(err)), 400


def requested_fields(fields):
    fields_dict = {}
    provided_fields_list = fields.split(",")
    for field in provided_fields_list:
        fields_dict[field] = True

    return fields_dict
