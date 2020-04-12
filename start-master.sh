#!/usr/bin/env bash
nohup python3 cli.py data-mine --frequency=15 &
nohup python3 cli.py data-process --frequency=15 &
nohup python3 cli.py trade --frequency=240 &
nohup python3 cli.py notify --frequency=240 &
