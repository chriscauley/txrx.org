#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PROJECT_ROOT=$DIR/../

for d in `ls $PROJECT_ROOT.dev`
do
    cd  $PROJECT_ROOT.dev/$d
    printf "updating $(pwd) ... ... "
    git pull
done

cd $PROJECT_ROOT
echo `date`>> _pullall.log
