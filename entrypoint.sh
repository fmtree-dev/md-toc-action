#!/bin/sh -l
md_toc_dir=$1
echo $md_toc_dir
ls
echo "::set-output name=success::true"