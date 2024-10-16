# TL;DR

[Swagger](https://swagger.io/getting-started-with-swagger-i-what-is-swagger/) specification of indexd's REST API

## Swagger Tools

### Editing
Use swagger's editor to update swagger.yaml and swagger.json using one of the following:
* [online editor](https://editor.swagger.io/)
* [Docker image](https://hub.docker.com/r/swaggerapi/swagger-editor/) - `docker run -d -p 80:8080 swaggerapi/swagger-editor`
* or pull the editor code from [github](https://github.com/swagger-api/swagger-editor), and `npm start` an editor locally.

### Publishing
Publish API documentation with the [swagger-ui](https://github.com/swagger-api/swagger-ui) - also easily launched with docker: `docker run -p 80:8080 -e SWAGGER_JSON=/foo/swagger.json -v /bar:/foo swaggerapi/swagger-ui`

Alternatively, the `openapis/openapi-index.html` file uses rapidoc to generate an interactive document from the `swagger.yaml` file. Many IDEs have an internal web server that can be used to serve this file. In PyCharm, opening the file will provide options to view the page in internal or external browsers.  
## OpenAPI Spec

The swagger definition format has been open sourced as the OpenAPI Specification administered by the Linux Foundation.  As of writing this the latest spec defining the structure and elements of a swagger.yaml file is [version 3](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md).
