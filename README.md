========
TXRX Labs Website
========

Install required system packages. This will vary from distribution to distribution.

```bash
apt-get install python-dev git-core python-pip libpng-dev libjpeg-dev
```

Now get the sourcecode from github. If you forked the source code use your own url (replace chriscauley with your github username).

```bash
git clone https://github.com/chriscauley/txrx.org
cd txrx.org
```

Install the python requirements.

```bash
pip install -r config/requirements.txt
```

Copy the dummy settings file to local.py

```bash
cp txrx/settings/dummy.py txrx/settings/local.py
```

Author
======
Chris Cauley
