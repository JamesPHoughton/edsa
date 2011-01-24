#!/bin/sh

EDSA_INSTALL_DIR=${EDSA_INSTALL_DIR:-"/usr/share/edsa"}

cd $EDSA_INSTALL_DIR/edsa

kill -9 `cat daemon_pid`
pkill -P `cat server_pid`
kill -9 `cat server_pid`

rm daemon_pid
rm server_pid

echo "EDSA client stopped."

