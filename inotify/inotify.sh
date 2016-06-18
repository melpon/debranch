#!/bin/bash

cd `dirname $0`

while true; do
    if ! inotifywait waiting -e attrib -e create -t 60; then
        echo "inotifywait failed" 1>&2
        exit 1
    fi

    while true; do
        COMMAND=`ls waiting/ -1 -t -r | head -n 1`

        if [ -z "$COMMAND" ]; then
            break
        fi

        START_AT=`date -r waiting/$COMMAND +%Y%m%d%H%M.%S`
        rm waiting/$COMMAND

        mkdir -p logs/$COMMAND

        echo "---- start ./scripts/$COMMAND.sh at $START_AT"
        ./scripts/$COMMAND.sh > logs/$COMMAND/stdout 2>logs/$COMMAND/stderr
        RESULT=$?
        echo "---- end ./scripts/$COMMAND.sh result=$RESULT"
        echo $? > logs/$COMMAND/status
        touch -t "$START_AT" logs/$COMMAND/last_queued_time
    done
done
