#!/bin/bash
# Executed at the root of the project

echo "=====> run scripts/gen_example_proto.sh"
bash scripts/gen_example_proto.sh

python_file_name_list=("gen_p2p_code.py" "gen_simple_code.py" "gen_text_comment_code.py" "gen_validate_code.py" "p2p_validate_by_comment_gen_code.py")
echo ""
for python_file_name in "${python_file_name_list[@]}"
do
  cd "example" || exit
  echo "=====> run  example/$python_file_name"
  uv run python "$python_file_name"
  cd ..
done