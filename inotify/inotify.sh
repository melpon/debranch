#!/bin/bash

# 二重起動の防止
PROCS=`pgrep $(basename $0)`
if [ `echo $PROCS | wc -w` -ge 2 ]; then
    echo "already running `basename $0`"
    exit 1
fi

cd `dirname $0`

while true; do
    inotifywait waiting -e attrib -e create -t 60

    while true; do
        COMMAND=`ls waiting/ -1 -t -r | head -n 1`

        if [ -z "$COMMAND" ]; then
            break
        fi

        START_AT=`date -r waiting/$COMMAND +%Y%m%d%H%M.%S`
        rm waiting/$COMMAND

        mkdir -p logs/$COMMAND

        echo "---- start ./scripts/$COMMAND.sh at $START_AT"
        ./fork.sh ./scripts/$COMMAND.sh > logs/$COMMAND/stdout 2>logs/$COMMAND/stderr
        RESULT=$?
        echo "---- end ./scripts/$COMMAND.sh result=$RESULT"
        echo $? > logs/$COMMAND/status
        touch -t "$START_AT" logs/$COMMAND/last_queued_time
    done
done
