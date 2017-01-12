#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PROJECT_ROOT=$DIR/../

cd $PROJECT_ROOT
bash server/pullall.sh

cd $PROJECT_ROOT/.dev/unrest/; gulp>/dev/null
cd $PROJECT_ROOT/.dev/drop/; gulp>/dev/null
cd $PROJECT_ROOT; gulp>/dev/null

python $PROJECT_ROOT/manage.py collectstatic --noinput>/dev/null
python $PROJECT_ROOT/manage.py compress>/dev/null

bash $PROJECT_ROOT/server/uwsgi.sh
