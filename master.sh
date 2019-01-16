#!/usr/bin/env bash
python wolftrader/cli.py "data_mine" &
python wolftrader/cli.py "data_process" &
python wolftrader/cli.py "notify" &
python wolftrader/cli.py "trade" &
