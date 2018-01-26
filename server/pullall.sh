#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PROJECT_ROOT=$DIR/../

for d in django-drop # django-airbrake-lite dj-stripe lablackey unrest django-unrest-comments django-unrest-media
do
    cd  ~/$d -P
    unset GIT_DIR
    printf "updating $(pwd) ... ... "
    git pull
done

cd $PROJECT_ROOT
echo `date`>> _pullall.log
