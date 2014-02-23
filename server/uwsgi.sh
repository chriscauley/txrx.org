DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if pidof uwsgi>/dev/null
then
    kill -HUP `cat /tmp/uwsgi.pid`
    echo "uwsgi reset"
else
    /usr/bin/uwsgi-core -M -x $DIR/../uwsgi.xml --plugin python&&
    echo "uwsgi wasn't running, but it is now!"
fi

exit 0
