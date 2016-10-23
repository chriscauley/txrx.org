ssh txrxlabs.org 'pg_dump txrx --username=postgres> dump.sql'
scp txrxlabs.org:dump.sql .
dropdb txrx --username=postgres
createdb txrx --username=postgres
psql --username=postgres txrx < dump.sql
./manage.py migrate --noinput
