#!/bin/sh

FILE=`readlink -f $0`
DIRNAME=`dirname $FILE`

PIDFILE=$DIRNAME/server.pid

echo $PIDFILE

ADDRESS=127.0.0.1:8002
LOGFILE=$DIRNAME/server.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=4
case "$1" in
    "stop" )
        if [ -f $PIDFILE ]; then
            kill `cat -- $PIDFILE`
            rm -f -- $PIDFILE
        fi
    ;;
    "" | "fg" )
        if [ -f $PIDFILE ]; then
            kill `cat -- $PIDFILE`
            rm -f -- $PIDFILE
        fi

        if [ "$1" = "fg" ]; then
            $DIRNAME/manage.py run_gunicorn --bind=$ADDRESS \
                --workers=$NUM_WORKERS --log-level=debug \
                --log-file=$LOGFILE 2>>$LOGFILE
        else
            $DIRNAME/manage.py run_gunicorn --bind=$ADDRESS \
                --pid=$PIDFILE --workers=$NUM_WORKERS \
                --log-level=debug --log-file=$LOGFILE \
                2>>$LOGFILE --daemon
        fi
esac
