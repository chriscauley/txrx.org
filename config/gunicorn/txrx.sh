#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/txrx.log
NUM_WORKERS=8
# user/group to run as
USER=website
GROUP=website
ADDRESS=127.0.0.1:8100
TIMEOUT=179
cd /home/website/txrx.org/src
source ../env/bin/activate
#exec gunicorn_django -b $ADDRESS -w $NUM_WORKERS \
#  --user $USER --group $GROUP --timeout $TIMEOUT \
#  --log-level debug --log-file $LOGFILE 2>>$LOGFILE
gunicorn txrx.wsgi:application