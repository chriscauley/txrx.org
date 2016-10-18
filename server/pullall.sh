#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PROJECT_ROOT=$DIR/../../

for d in lablackey django-drop unrest django-unrest-media
do
    cd  $PROJECT_ROOT$d
    printf "updating $d ... ... "
    git pull
done
