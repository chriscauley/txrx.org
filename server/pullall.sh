#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PROJECT_ROOT=$DIR/../../

for d in `ls .dev`
do
    #cd  $PROJECT_ROOT$d
    printf "updating $d ... ... "
    git pull
done
