#!/bin/bash

PRG="$0"
PRGDIR=`dirname "$PRG"` && PRGDIR=`cd "$PRGDIR" >/dev/null; pwd`
cd "$PRGDIR/.."

if [ ! -d "venv" ]; then
    echo "Start to install Python3 venv and requirements!"
    virtualenv -p python3 venv
fi

source ./venv/bin/activate
pip3 install -r requirements.txt
deactivate
