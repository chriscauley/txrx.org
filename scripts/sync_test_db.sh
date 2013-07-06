#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="$DIR/.."

FORCE="force"

echo $1

if [[ $FORCE -eq $FORCE ]]; then
    echo "This program will backup txrx.db and replace it with anon.db"
    echo "If you are not using 'txrx/txrx.db', then this program will not do anything."
    read -p "Are you sure? Type \"y\" to continue: " -n 1 -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
	exit
    fi
fi
cd $SOURCE_DIR

FILE="txrx/txrx.db"
if [ -f $FILE ]; then mv $FILE txrx/old.db; fi
echo
scp development@dev.txrxlabs.org:/home/development/anon.db txrx/txrx.db
echo -e "\nOld db has been backed up as txrx/old.db and the anon database has been created."
echo "Please use username \"admin\" and password \"hackerspace\" for superuser access to your site."
echo