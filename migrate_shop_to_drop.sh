dropdb txrx --username=postgres; createdb txrx --username=postgres; psql --username=postgres txrx < dump.sql
python manage.py dumpdata shop >_shop.json
python _shop_to_drop.py
python manage.py migrate drop --noinput
python manage.py loaddata _drop.json
python manage.py migrate shop 0001 --fake --noinput
python manage.py migrate --noinput
