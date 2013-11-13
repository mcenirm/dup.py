#!/bin/bash
set -o errexit
set -o nounset
set -o noclobber

SRC=ex-src
SRC2=ex-src2
DST=ex-dst

mkdir -p "$SRC" "$DST"
ln -s "$SRC" "$SRC2"

cat >| ex.dup <<EOF
#!${PWD}/dup.py
${PWD}/${SRC}  ${PWD}/${DST}
EOF

good_list=(
  ${SRC}/simple.txt
  ${SRC}/foo/bar/subdirectories.txt
  ${SRC2}/symlink.txt
)

bad_list=(
  /does/not/exist.txt
)

for good in "${good_list[@]}" ; do
  mkdir -p $(dirname "$good")
  if ! [[ -e "$good" ]] ; then
    echo " $good" > "$good"
  fi
done

./ex.dup "${good_list[@]}" "${bad_list[@]}"

