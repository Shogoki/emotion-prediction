#!/bin/bash

docker run -it -v $PWD:/swag --rm openapitools/openapi-generator-cli generate -i /swag/backend.yml -g python-flask -o /swag/api


