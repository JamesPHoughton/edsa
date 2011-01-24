#!/bin/sh

EDSA_INSTALL_DIR=${EDSA_INSTALL_DIR:-"/usr/share/edsa"}

cd $EDSA_INSTALL_DIR/edsa

./daemon.py >> daemons.log &
echo $! > daemon_pid
./manage.py runserver >> server.log &
echo $! > server_pid
firefox http://localhost:8000

echo "EDSA client started."

