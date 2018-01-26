#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PROJECT_ROOT=$DIR/../

cd $PROJECT_ROOT
#python manage.py migrate >/dev/null # manually migrate txrx for now
gulp > /dev/null

MIGRATIONS="$(bash server/pullall.sh|grep migrations/00)"

# manually migrate external packages for now
# if [[ ! -z $MIGRATIONS ]];
#     then
#     echo "migrating because of git pull output:"
#     echo $MIGRATIONS
#     cd $PROJECT_ROOT
#     python manage.py migrate >/dev/null
# fi

# cd $PROJECT_ROOT/.dev/unrest/; gulp>/dev/null
cd $PROJECT_ROOT/.dev/drop/; gulp>/dev/null
cd $PROJECT_ROOT; gulp>/dev/null

python $PROJECT_ROOT/manage.py collectstatic --noinput>/dev/null
python $PROJECT_ROOT/manage.py compress>/dev/null

bash $PROJECT_ROOT/server/uwsgi.sh
