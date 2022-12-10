#!/bin/bash
poetry run python -m grpc_tools.protoc \
  --mypy_grpc_out=./ \
  --mypy_out=./ \
  --python_out=./ \
  --grpc_python_out=./ \
  -I protos $(find ./protos -name '*.proto')
