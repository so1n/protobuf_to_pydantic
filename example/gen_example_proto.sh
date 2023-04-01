# set venv
export VENV_PREFIX=""
if [ -d '../venv' ] ; then
    export VENV_PREFIX="../venv/bin/"
fi
if [ -d '../.venv' ] ; then
    export VENV_PREFIX="../.venv/bin/"
fi

echo 'use venv path:' ${VENV_PREFIX}

# gen python protos code path
target_p='example_proto_python_code'
# project proto path
source_p='example_proto'
# service
service_list=("demo" "validate" "p2p_validate" "common")
plugin_p='../protobuf_to_pydantic/plugin/main.py'


rm -r "${target_p:?}/${source_p:?}"*
mkdir -p "${target_p:?}/${source_p:?}"
chmod u+x $plugin_p

for service in "${service_list[@]}"
do
  mkdir -p "${target_p:?}/${source_p:?}/${service:?}"
  echo  "from proto file:" $source_p/"$service"/*.proto "gen proto py file to" $target_p/$source_p
  ${VENV_PREFIX}python -m grpc_tools.protoc \
    --plugin=protoc-gen-custom-plugin=$plugin_p --custom-plugin_out=config_path=plugin_config.py:./$target_p/ \
    --python_out=./$target_p \
    --grpc_python_out=./$target_p \
    --mypy_grpc_out=./$target_p \
    --mypy_out=./$target_p \
    -I. \
    $source_p/"$service"/*.proto

  touch $target_p/$source_p/"$service"/__init__.py
  # fix grpc tools bug
  sed -i "s/from protos.$service import/from . import/" $target_p/$source_p/$service/*.py
  sed -i "s/from example_proto./from example.example_proto_python_code.example_proto./" $target_p/$source_p/$service/*.py
done
