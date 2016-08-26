#dropdb txrx --username=postgres; createdb txrx --username=postgres; psql --username=postgres txrx < dump.sql

cd dev
git clone https://github.com/chriscauley/django-drop.git
git clone https://github.com/chriscauley/django-shop.git
cd lablackey; git pull; cd ..
rm lablackey
ln -s /home/django/lablackey/lablackey/ .
cd shop; git checkout migrate_to_drop; cd ..

sudo pip install django-polymorphic==0.9.2
sudo rm -rf src/django-shop/ /usr/local/lib/python2.7/dist-packages/shoppython manage.py dumpdata shop >_shop.json
python manage.py dumpdata shop >_shop.json
python _shop_to_drop.py
python manage.py migrate drop --noinput
python manage.py loaddata _drop.json
python manage.py migrate shop 0001 --fake --noinput
python manage.py migrate --noinput
