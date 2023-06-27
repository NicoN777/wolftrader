#!/bin/bash

WOLF_ROOT=$(pwd)
echo "Creating directories..."
mkdir -p ${WOLF_ROOT}/logs ${WOLF_ROOT}/db
touch ${WOLF_ROOT}/logs/wolflog.log

echo "Create a virtual environment..."
python3 -m venv ${WOLF_ROOT}/wolfie-venv

echo "Create the sqlite db..."
sqlite3 ${WOLF_ROOT}/db/Coinbase.db ".read ${WOLF_ROOT}/db/create-schema.ddl"

WOLF_CONFIG_FILE="${WOLF_ROOT}/wolftrader/resources/conf/wolfie.ini"
echo "Please add the required configurations to ${WOLF_CONFIG_FILE}"




