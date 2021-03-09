#!/bin/sh -l
md_toc_dir=$1
echo "custom directory: $md_toc_dir"
pydoc fmtree
echo "::set-output name=success::true"