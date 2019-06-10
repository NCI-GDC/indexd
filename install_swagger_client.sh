#!/bin/bash

curl -LO https://oss.sonatype.org/content/repositories/releases/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar
java -jar swagger-codegen-cli-2.3.1.jar generate -i openapis/swagger.yaml -l python -o swagger_client

pushd swagger_client
python setup.py install
popd
