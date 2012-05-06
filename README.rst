========
TXRX Labs Website
========

Depends on the LabLackey git repository. After cloning, cd into txrx.org and run:

    $ git submodule update --init --recursive


Then install all python requirements with:

    $ sudo apt-get install python-imaging    # package manager may vary
    
    $ sudo pip install -r requirements.txt

Create database with:

    $ cd txrx
    
    $ python manage.py syncdb    # You will be prompted to create a super user
    
    $ python manage.py migrate

Database is stored in txrx.db by default. Feel free to delete and recreate.
Run devserver with

    $ python manage.py runserver 0.0.0.0:8000

Website can be accessed through localhost:8000
Admin is at /admin 

Author
======
Chris Cauley
