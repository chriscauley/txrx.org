#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INI="$DIR/uwsgi.ini"
UWSGI="$DIR/../.venv/bin/uwsgi"

PID=`cat /tmp/txrx.pid 2>/dev/null`

if kill -HUP "$PID" 2>/dev/null
then
    echo "uwsgi reset (HUP $PID)"
else
    echo "uwsgi wasn't running, starting it now"
    "$UWSGI" --ini "$INI" &
fi

exit 0
