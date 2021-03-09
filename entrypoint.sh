#!/bin/sh -l
md_toc_dir=$1
echo $md_toc_dir
ls
touch debug.txt
ls
echo "::set-output name=success::true"