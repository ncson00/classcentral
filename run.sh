#!/bin/bash

while read f; do
	python3 translate_tag.py -d $f
	python3 translate_nested_tag.py -d $f -n p a h1 h2 h3
done <file_dir_tmp.txt