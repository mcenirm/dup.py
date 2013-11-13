#!/bin/bash
set -o errexit
set -o nounset
set -o noclobber

PATH=$PWD:$PATH ./ex.dup foo

