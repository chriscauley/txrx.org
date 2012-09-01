#!/bin/bash
set -e
LOGFILE=/home/chriscauley/django-projects/txrx.org/log/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
USER=chriscauley
GROUP=chriscauley
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn_django -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE \
    --settings=txrx.settings \
    --pythonpath=`pwd`
