#!/usr/bin/env bash
nohup python3 cli.py data-mine --frequency=10 &
nohup python3 cli.py data-process --frequency=10 &
nohup python3 cli.py trade --frequency=480 &
nohup python3 cli.py notify --frequency=480 &
