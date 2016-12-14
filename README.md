TXRX Labs Website
========

Install required system packages. This will vary from distribution to distribution.

```bash
apt-get install python-dev git-core python-pip libpng-dev libjpeg-dev python-psycopg2 libpq-dev
```

Now get the sourcecode from github. If you forked the source code use your own url (replace chriscauley with your github username).

```bash
git clone https://github.com/chriscauley/txrx.org
cd txrx.org
```

Install the python requirements.

```bash
pip install -r requirements.txt
```

You can create the database one of two ways. Ask chriscauley for the password to development@dev.txrxlabs.org and then run the following command:

```bash
bash scripts/sync_test_db.sh
```

Hit 'y'  when prompted and enter the password. This will download the latest copy of the database (fully anonymized).

Aternately you can create the database by running the following two commands.

```bash
python manage.py syncdb
python manage.py migrate
```

This will create an empty database and you will be prompetd to create a superuser. 

Author
======
Chris Cauley
