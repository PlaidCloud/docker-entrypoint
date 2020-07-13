#!/bin/bash
set -e
pid=""
trap quit TERM INT
quit() {
  if [ -n "$pid" ]; then
    kill $pid
  fi
}

mkdir -p /.devspace
touch /.env
while true; do
    while read p; do
        export $p
    done < /.env
    if [[ "$DEBUGGER_ENABLED" == "false" || "$DEBUGGER_EDITOR" == "vscode" ]]; then
        setsid "$@" &
        pid=$!
        echo "$pid" > /.devspace/devspace-pid
        set +e
        wait $pid
    elif [[ "$DEBUGGER_EDITOR" == "pycharm" ]] || [[ "$DEBUGGER_EDITOR" == "wing" ]]; then
        echo "Waiting for debug session to start."
        until [ -f /.devspace/devspace-pid ]
        do
            sleep 3
        done
        echo "Debug session started. Waiting until exit."
        pid=$(cat /devspace-pid)
        while [ -e /proc/$pid ]
        do
            sleep 3
        done
    fi
    exit_code=$?
    set -e
    if [ -f /.devspace/devspace-pid ]; then
        exit $exit_code
    fi
    echo "Restart container"
done
