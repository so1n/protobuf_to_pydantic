export VENV_PREFIX=""
if [ -d '../venv' ] ; then
    export VENV_PREFIX="../venv/bin/"
fi
if [ -d '../.venv' ] ; then
    export VENV_PREFIX="../.venv/bin/"
fi


echo "=====> run $(pwd)/gen_rpc.sh"
bash ./gen_rpc.sh

directory_list=("simple_example" "text_comment_example" "validate_example" "p2p_validate_example")
echo ""
VENV_PREFIX="../${VENV_PREFIX}"
echo 'use venv path:' ${VENV_PREFIX}
for directory in "${directory_list[@]}"
do
  cd "$(pwd)/$directory" || exit
  echo "=====> run  $(pwd)/$directory/gen_code.py"
  ${VENV_PREFIX}python gen_code.py
  cd ..
done
