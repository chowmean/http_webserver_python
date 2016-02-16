#!/bin/bash
if [ "$1" = "install" ]
then
	sudo apt-get install redis-server
	sudo pip install redis
elif [ "$1" = "run" ]
then
	redis-server & python asynchttpserver.py $2 $3
fi
exit 0
