#!/bin/bash


# optimise everything directly in $_SOURCE_DIR, place results in $_PROCESS_DIR
# Use parallel where possible; optimisation can be slow on large/complex images.
#
# TODO: import vars from main TOML, possibly configure vpype vi that, or subset. 
_SOURCE_DIR="../output"
_PROCESS_DIR="$_SOURCE_DIR/processed"
vpype_flags="linemerge linesort reloop linesimplify"

find $_SOURCE_DIR -maxdepth 1 -iname "*.svg" | parallel 'basename {}' | parallel vpype read $_SOURCE_DIR/{} $vpype_flags write $_PROCESS_DIR/{}
