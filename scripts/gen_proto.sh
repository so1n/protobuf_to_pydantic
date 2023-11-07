#!/bin/bash
source_p='protos'
target_p=$1

echo $target_p
poetry run python -m grpc_tools.protoc \
  --mypy_out=$target_p \
  --python_out=$target_p \
  -I. $source_p/*.proto
