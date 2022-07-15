export VENV_PREFIX=""
if [ -d '../venv' ] ; then
    export VENV_PREFIX="../venv/bin/"
fi
if [ -d '../.venv' ] ; then
    export VENV_PREFIX="../.venv/bin/"
fi

echo 'use venv path:' ${VENV_PREFIX}

echo "=====> run $(pwd)/gen_rpc.sh"
chmod +x gen_rpc.sh
bash ./gen_rpc.sh

directory_list=("simple_example" "text_comment_example" "validate_example")
VENV_PREFIX="../${VENV_PREFIX}"
for directory in "${directory_list[@]}"
do
  cd "$(pwd)/$directory" || exit
  echo "=====> run  $(pwd)/$directory/gen_code.py"
  ${VENV_PREFIX}python gen_code.py
  cd ..
done
