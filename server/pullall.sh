#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PROJECT_ROOT=$DIR/../

for d in django-drop django-airbrake-lite dj-stripe lablackey Django-Next-Please unrest django-unrest-comments
do
    cd  ~/$d -P
    printf "updating $(pwd) ... ... "
    git pull
done

cd $PROJECT_ROOT
echo `date`>> _pullall.log
