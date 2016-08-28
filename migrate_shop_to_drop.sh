#dropdb txrx --username=postgres; createdb txrx --username=postgres; psql --username=postgres txrx < dump.sql

# on cloned server we need to restart postgres
# sudo su postgres
# /usr/lib/postgresql/9.1/bin/pg_resetxlog -f /var/lib/postgresql/9.1/main
# exit
# sudo /etc/init.d/postgresql start

sudo pip install django-polymorphic==0.9.2
sudo rm -rf src/django-shop/ /usr/local/lib/python2.7/dist-packages/shop

sudo su django
cd
git clone https://github.com/chriscauley/django-drop.git
git clone https://github.com/chriscauley/django-shop.git
cd txrx.org/dev
ln -s /home/django/django-shop/shop .
ln -s /home/django/django-drop/drop .
cd lablackey; git pull; cd ..
rm lablackey
ln -s /home/django/lablackey/lablackey/ .
cd shop; git checkout migrate_to_drop; cd ../..

emacs .git/config # set bare=false
git pull
python manage.py dumpdata shop >_shop.json
python _shop_to_drop.py
python manage.py migrate drop --noinput
python manage.py loaddata _drop.json
python manage.py migrate shop 0001 --fake --noinput
python manage.py migrate --noinput
rm -rf .static/bower/ur
bower install
python manage.py collectstatic
python manage.py compress
