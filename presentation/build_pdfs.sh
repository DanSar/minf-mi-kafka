#!/bin/bash

function convert_to_pdf {
  file=$1

  filename=$(basename "$file")
  basename="${filename%.*}"
  dir=$(dirname "$file")
  target="${basename}.pdf"

  echo $file

  inkscape -D -z --file="$file" --export-pdf="$dir/$target" 2>/dev/null
}

for file in *.svg; do
  convert_to_pdf $file
done

for file in **/*.svg; do
  convert_to_pdf $file
done
