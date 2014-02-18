#./manage.py dumpdata codrspace.pressitem thing>bu.json
scp chriscauley@old.txrxlabs.org:/home/chriscauley/dump.sql ~/
dropdb txrx --username=postgres;createdb txrx --username=postgres;psql --username=postgres txrx < ~/dump.sql
./manage.py migrate
./manage.py loaddata bu.json
rm -rf .media
mkdir .media
scp -r chriscauley@old.txrxlabs.org:/home/website/txrx.org/src/media/* .media/
