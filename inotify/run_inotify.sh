#!/bin/bash

cd `dirname $0`

if [ $# -lt 1 ]; then
    echo "$0 <command>"
    exit 1
fi

COMMAND=$1

QUEUED_TIME=`date`
QUEUED_TIME_UNIXTIME=`date -d "$QUEUED_TIME" +%s`
QUEUED_TIME_TIMESTAMP=`date -d "$QUEUED_TIME" +%Y%m%d%H%M.%S`
touch -t $QUEUED_TIME_TIMESTAMP waiting/$COMMAND

while true; do
    if [ -e logs/$COMMAND/last_queued_time ]; then
        LAST_QUEUED_TIME_UNIXTIME=`date -r logs/$COMMAND/last_queued_time +%s`
        if [ $LAST_QUEUED_TIME_UNIXTIME -ge $QUEUED_TIME_UNIXTIME ]; then
            exit `cat logs/$COMMAND/status`
        fi
        inotifywait logs/$COMMAND/last_queued_time -e attrib -e create -t 60
    fi
    sleep 1
done
