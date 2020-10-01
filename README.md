TXRX Labs Website
========

Install required system packages. **NOTE**  This will vary from distribution to distribution.

```bash
apt-get install python-dev git-core python-pip libpng-dev libjpeg-dev python-psycopg2 postgresql memcached python-memcache
pip install pip --update
```

Currently there are a lot of experimental packages which I am actively working on. Clone these from the github by simply pasting this into the shell. You may want to place this in a subdirectory to store all these. They will be symbolically linked later and can be updated with a single command.

```bash
git clone http://github.com/chriscauley/lablackey
git clone http://github.com/chriscauley/unrest
git clone http://github.com/chriscauley/django-drop
git clone http://github.com/chriscauley/django-unrest-comments
git clone http://github.com/chriscauley/django-airbrake-lite
git clone http://github.com/chriscauley/dj-stripe
git clone http://github.com/chriscauley/Django-Next-Please
mkdir .dev
ln -s `pwd`/lablackey/lablackey .dev
ln -s `pwd`/unrest .dev
ln -s `pwd`/django-drop/drop .dev
ln -s `pwd`/django-unrest-comments/unrest_comments .dev
ln -s `pwd`/django-airbrake-lite/airbrake .dev
ln -s `pwd`/dj-stripe/djstripe .dev
ln -s `pwd`/Django-Next-Please/NextPlease .dev
```

Now just get the sourcecode from github. If you have forked the source code use your own url (just replace chriscauley with your github username). Modify the last line to represent the ABSOLUTE path to the .dev folder created above.

```bash
git clone https://github.com/chriscauley/txrx.org
cd txrx.org
ln -s /path/to/.dev .
```

Install the python requirements. You should consider putting this into a virtual environment.

```bash
pip install -r requirements.txt
```

To get a test copy of the live database, you'll have to email me. Alternately you can create your own database by running the following two commands.

```bash
python manage.py migrate
```

This will create an empty database and you will be prompetd to create a superuser.

Author
======
Chris Cauley
