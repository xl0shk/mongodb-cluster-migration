#!/bin/bash

PROJECT="mongodb-cluster-migration"
PIDFILE="bin/api.pid"

PRG="$0"
PRGDIR=`dirname "$PRG"` && PRGDIR=`cd "$PRGDIR" >/dev/null; pwd`
cd "$PRGDIR/.."


function check_venv() {
    if [ ! -d "venv" ]; then
        echo "Start to install Python3 venv and requirements!"
        bash ./bin/create_python3_venv.sh
    fi;
}


function start() {
    echo "Enter Python3 venv"
    source ./venv/bin/activate
    echo "Starting $PROJECT project ..."
    gunicorn -w 1 -b 0.0.0.0:5000 api:app -p $PIDFILE -D
    _PID=`cat $PIDFILE 2>/dev/null`
    echo "$PROJECT Project ($_PID) start Successfully."
    exit 0
}


function stop() {
    echo "Stopping $PROJECT project..."
    if [ ! -f "$PIDFILE" ]; then
            echo "$PROJECT Project Never Starts."
            return
    fi
    _PID=`cat $PIDFILE 2>/dev/null`
    kill $_PID
    rm -f $PIDFILE
    echo "$PROJECT project is stopped!!!"
}


function restart() {
    echo "Restarting $PROJECT project..."
    stop
    sleep 2
    start
}


function help() {
        echo "$PROJECT Project Script"
        echo "Usage:"
        echo "  $0 start|stop|restart"
}


case $1 in
        start)
            check_venv
            start
            exit 0
            ;;
        stop)
            stop
            exit 0
            ;;
        restart)
           restart
            ;;
        *)
        help
        exit -1
        ;;
esac
