from __future__ import with_statement
from fabric.api import *
from fabric.contrib.files import exists
import os
from datetime import *

env.project = 'txrx.org'
env.git_server = 'github.com'
env.source_dir = 'txrx.org/src'
env.logs = "txrx.org/logs"
env.database = "txrx.org/database"
env.virtualenv = "txrx.org/env"
env.media = "txrx.org/media"
env.static = "txrx.org/static"
env.database_name = "txrx"

"""
Environments
"""
def sandbox():
    env.hosts = ['sandbox']
    
def production():
    env.hosts = ['classes.txrxlabs.org']

""" 
Local Tasks
"""
def setup_local():
    with lcd("../"):
        local("virtualenv --no-site-package env")
        local("pip -E env install django")

def freeze():
    local("pip -E ../env freeze > requirements.txt")
    
def local_dump():
    with lcd("../database"):
        local("pg_dump --clean %s > %s-%s.sql" % (env.database_name, env.database_name, date.today()))
        
def put_dump(db_filename):
    with lcd("../database"):
        put(db_filename, "%s/%s" % (env.database, db_filename))
        
def update_local():
    local("pip -E ../env install -r requirements.txt")
    
    
"""
Remote Tasks
"""
def install_packages():
    "Installs software supported at the OS level in perparation for the project"
    
    sudo("apt-get -y install python2.7 python-dev python-setuptools build-essential git-core nginx")
    sudo("apt-get -y build-dep python-psycopg2")
    sudo("easy_install pip")
    sudo("pip install virtualenv")
    # supervisord depends on elementtree but it's not a debian package anymore
    sudo("pip install elementtree")
    sudo("apt-get -y install supervisor")
    
def setup_project():
    "Does lots of the one-time stuff to make a project ready to deploy"
    #install_packages()

    with settings(warn_only=True):
        sudo("mkdir /var/log/gunicorn")
    sudo("chgrp website /var/log/gunicorn")
    sudo("chmod 775 /var/log/gunicorn")
    
    with settings(warn_only=True):
        run("mkdir %(project)s" % env)
        #run("mkdir %(virtualenv)s" % env)
        run("mkdir %(database)s" % env)
        run("mkdir %(logs)s" % env)
        run("mkdir %(media)s" % env)
        run("mkdir %(static)s" % env)

    
    
    run("virtualenv --no-site-packages %(virtualenv)s" % env)
    run("git clone git://%(git_server)s/chriscauley/%(project)s.git %(source_dir)s" % env)
    
    update_environment()
    
    
def update_environment():
    git_pull()
    run("pip install -r %(source_dir)s/requirements.txt" % env)
    
def setup_database():
    "You've got to do some stuff on your own here, but once that's done, run this"
    with cd(env.source_dir):
        with("source %(virtualenv)s/bin/activate" % env):
            run("./manage.py syncdb")
            run("./manage.py migrate")
        
def import_data(data='dbdump.json'):
    "Between setup_database() and here you'll have to TRUNCATE CASCADED the django_content_types table"
    with cd(env.source_dir):
        run("./manage.py loaddata database/%s" % data)
    
def update_config():
    git_pull()
    make_gunicorn_executable()
    update_gunicorn()
    update_nginx()
    update_cron()
        
def make_gunicorn_executable():
    with cd(env.source_dir):
        run("chmod +x config/gunicorn/txrx.sh" % env)
        
def restart_gunicorn():
    run("sudo /usr/bin/supervisorctl restart txrx" % env)
        
def update_gunicorn():
    run("sudo /usr/bin/supervisorctl stop txrx" % env)
    
    with cd(env.source_dir):
        sudo("cp config/supervisor/txrx.conf /etc/supervisor/conf.d/txrx.conf" % env)
        
    run("sudo /usr/bin/supervisorctl update")
    run("sudo /usr/bin/supervisorctl start txrx" % env)
        
def restart_nginx():
    sudo("/etc/init.d/nginx restart")
        
def update_nginx():
    with cd(env.source_dir):
        sudo("cp config/nginx/txrx /etc/nginx/sites-available" % env)
        
        if not exists("/etc/nginx/sites-enabled/txrx" % env):
            sudo("ln -s /etc/nginx/sites-available/txrx /etc/nginx/sites-enabled/txrx" % env)
        
    restart_nginx()
    
def update_cron():
    with cd(env.source_dir):
        sudo("cp config/crontab/txrx /etc/cron.d/txrx" % env)
        sudo("chown root /etc/cron.d/txrx" % env)
        sudo("touch /etc/cron.d/")
        
def git_pull(branch='master'):
    with cd(env.source_dir):
        run("git pull origin %s" % (branch, )) 

def collectstatic():
    run("cd txrx.org/src && ./manage.py collectstatic -v0 --noinput")
        
def deploy():
    git_pull()
    collectstatic()
    restart_gunicorn()
    
def db_overwrite(database_file):
    with cd(env.database):
        run("sudo -u postgres psql %s < %s" % (env.database_name, database_file))

def test():
    "Run the test suite and bail out if it fails"
    local("cd $(project_name); python manage.py test", fail="abort")

def db_dump():
    from django.conf import settings
    
    dbsettings = settings.DATABASES['default']
    
    with cd(env.database):
        run('export PGPASSWORD="%s"; pg_dump -U %s --host=localhost --clean -Fc -Z 9 %s > %s-%s.cbackup' \
            % (dbsettings['PASSWORD'], dbsettings['USER'], dbsettings['NAME'], dbsettings['NAME'], date.today()))


"""
Stuff I found and haven't yet copied correctly
"""
def deploy_version(version):
    "Specify a specific version to be made live"
    require('hosts', provided_by=[local])
    require('path')
    config.version = version
    run('cd $(path); rm releases/previous; mv releases/current releases/previous;')
    run('cd $(path); ln -s $(version) releases/current')
    restart_webserver()
    
def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    require('hosts', provided_by=[local])
    require('path')
    run('cd $(path); mv releases/current releases/_previous;')
    run('cd $(path); mv releases/previous releases/current;')
    run('cd $(path); mv releases/_previous releases/previous;')
    restart_webserver()    

    
