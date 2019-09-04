DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PROCESSES=3
if [ -a $DIR/staging ]
then
    export PROCESSES=1
fi

if cat /tmp/txrx.pid 2> /dev/null
then
    kill -HUP `cat /tmp/txrx.pid`
    echo "uwsgi reset"
else
    source .venv/bin/activate
    echo "uwsgi wasn't running, starting it now"
    uwsgi -M -x $DIR/../uwsgi.xml &&
fi

exit 0
