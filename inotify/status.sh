#!/bin/bash

# inotify.shが生きてるかどうか
PIDS=`pgrep -o inotify.sh`
if pgrep -o inotify.sh > /dev/null; then
    echo "STATUS: running"

    echo ""
    echo "PSTREE:"
    for PID in $PIDS; do
        pstree -alp $PID
    done
else
    echo "STATUS: stopped"
fi

echo ""

echo "QUEUED TASKS:"
for FILE in `ls -tr waiting`; do
    TIME=`date -r waiting/$FILE "+%Y-%m-%d %H:%M:%S"`
    echo "    $TIME     $FILE"
done
