DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PROCESSES=3
if [ -a $DIR/staging ]
then
    export PROCESSES=1
fi

echo /usr/bin/uwsgi-core -M -x $DIR/../uwsgi.xml --plugin python -p $PROCESSES

if cat /tmp/uwsgi.pid
then
    kill -HUP `cat /tmp/uwsgi.pid`
    echo "uwsgi reset"
else
    /usr/bin/uwsgi-core -M -x $DIR/../uwsgi.xml --plugin python -p $PROCESSES &&
    ps aux|grep uwsgi
    echo "uwsgi wasn't running, but it is now!"
fi

exit 0
