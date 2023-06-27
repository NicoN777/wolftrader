#!/usr/bin/env bash
WOLF_ROOT=$(pwd)
source ${WOLF_ROOT}/wolfie-venv/bin/activate
APP_NAME=wolftrader
export PYTHON_PATH="${WOLF_ROOT}/${APP_NAME}"
nohup python3 ${APP_NAME}/cli.py data-mine --frequency=15 &
echo $! > data-mine.pid
nohup python3 ${APP_NAME}/cli.py data-process --frequency=15 &
echo $! > data-process.pid
nohup python3 ${APP_NAME}/cli.py trade --frequency=240 &
echo $! > trade.pid
nohup python3 ${APP_NAME}/cli.py notify --frequency=240 &
echo $! > notify.pid
