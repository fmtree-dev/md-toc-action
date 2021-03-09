#!/bin/sh -l
md_toc_dir=$1
echo "custom directory"
echo $md_toc_dir
ls
touch debug.txt
ls
echo $(ls)
echo "::set-output name=success::true"