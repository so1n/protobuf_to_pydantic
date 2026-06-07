#!/bin/bash
# Executed at the root of the project
proto_target=$(poetry run python -c "from google.protobuf import __version__;from protobuf_to_pydantic._pydantic_adapter import is_v1;target_p = 'proto' if __version__ > '4.0.0' else 'proto_3_20';target_p += '_pydanticv1' if is_v1 else '_pydanticv2';print(target_p)")
echo "Using proto_target: ${proto_target}"
# gen python protos code path
target_p="example/$proto_target"
# project proto path
source_p="example/example_proto"
# service
service_list=("demo" "validate" "p2p_validate" "common" "p2p_validate_by_comment")


rm -r "${target_p:?}/${source_p:?}"*
mkdir -p "${target_p:?}/${source_p:?}"

for service in "${service_list[@]}"
do
  mkdir -p "${target_p:?}/${source_p:?}/${service:?}"
  echo  "from proto file:" $source_p/"$service"/*.proto "gen proto py file to" $target_p/$source_p
  poetry run python -m grpc_tools.protoc \
    --protobuf-to-pydantic_out=config_path=example/plugin_config.py:./$target_p/ \
    --python_out=./$target_p \
    --mypy_out=./$target_p \
    -I. \
    $source_p/"$service"/*.proto

  touch $target_p/$source_p/"$service"/__init__.py
  # fix grpc tools bug
  sed -i "s/from protos.$service import/from . import/" $target_p/$source_p/$service/*.py
  sed -i "s/from example_proto./from example.$proto_target.example.example_proto./" $target_p/$source_p/$service/*.py
  sed -i "s/from example.example_proto/from example.$proto_target.example.example_proto/" $target_p/$source_p/$service/*.py
done

enum_desc_proto_file_list=("$source_p/common/single.proto" "$source_p/demo/demo.proto")
for proto_file in "${enum_desc_proto_file_list[@]}"
do
  service=$(basename "$(dirname "$proto_file")")
  echo  "from proto file:" "$proto_file" "gen enum desc pydantic code to" $target_p/$source_p
  poetry run python -m grpc_tools.protoc \
    --protobuf-to-pydantic_out=config_path=example/enum_desc_plugin_config.py:./$target_p/ \
    -I. \
    "$proto_file"

  sed -i "s/from example_proto./from example.$proto_target.example.example_proto./" $target_p/$source_p/$service/*_enum_desc_p2p.py
  sed -i "s/from example.example_proto/from example.$proto_target.example.example_proto/" $target_p/$source_p/$service/*_enum_desc_p2p.py
done
