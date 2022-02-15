import json
import pkg_resources

from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPIValidationError
from openapi_spec_validator.readers import read_from_filename

import openapis


def test_valid_openapi():
    filename = pkg_resources.resource_filename(openapis.__name__, 'swagger.yaml')
    spec, url = read_from_filename(filename)

    if not isinstance(spec, dict):
        raise OpenAPIValidationError('root node is not a mapping')
    # ensure the spec is valid JSON
    spec = json.loads(json.dumps(spec))

    validate_spec(spec, url)
