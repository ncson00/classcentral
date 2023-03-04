#!/bin/bash

while read f; do
	python3 translate_tag.py -d $f
done <file_dir.txt
