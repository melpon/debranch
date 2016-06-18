#!/bin/bash

cd `dirname $0`

while true; do
    if ! inotifywait waiting -e attrib -e create; then
        echo "inotifywait failed" 1>&2
        exit 1
    fi

    COMMAND=`ls waiting -1 -t -r | head -n 1`

    mkdir -p logs/$COMMAND

    ./scripts/$COMMAND.sh > logs/$COMMAND/stdout 2>logs/$COMMAND/stderr
    echo $? > logs/$COMMAND/status

    rm waiting/$COMMAND
done
