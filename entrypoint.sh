#!/bin/sh -l
# Initialize and Print Parameters
md_toc_dir=$1
echo "custom directory: $md_toc_dir"
python main.py --custom_dir $md_toc_dir
cat ./data/OSCP/Exercises/README.md
cat ./data/OSCP/README.md
cat ./data/README.md
echo "::set-output name=success::true"