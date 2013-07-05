#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="$DIR/.."

cd $DIR

rm anon.db -f
python $SOURCE_DIR/manage.py syncdb --database=anon --noinput > /dev/null
python $SOURCE_DIR/manage.py migrate --database=anon --noinput > /dev/null
python $SOURCE_DIR/manage.py dumpdata>backup.json
python $SOURCE_DIR/manage.py loaddata --database=anon backup.json
echo `ls anon.db -al`

echo "drop table django_session;"|sqlite3 anon.db #>/dev/null
echo "drop table paypal_ipn;"|sqlite3 anon.db #>/dev/null
echo "drop table django_admin_log;"|sqlite3 anon.db #>/dev/null
echo "drop table thumbnail_kvstore;"|sqlite3 anon.db #>/dev/null

echo `ls anon.db -al`

python $SOURCE_DIR/manage.py anonymize