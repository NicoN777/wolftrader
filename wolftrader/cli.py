"""
    Main point of entry for wolftrade

    To run:
        python cli.py [args]
        "visualize"
        "trade"
"""
import sys
import time
from wolf import mine, process, notify, trade
#
if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'data_mine':
            while True:
                mine()
                time.sleep(600)
        elif sys.argv[1] == 'data_process':
            while True:
                process()
                time.sleep(600)
        elif sys.argv[1] == 'notify':
            while True:
                notify()
                time.sleep(3600*4)
        elif sys.argv[1] == 'trade':
            while True:
                trade()
                time.sleep(3600*8)
        else:
            print('Parameter not recognized')
    else:
        print ("The fuck you talkin 'bout playa")


def miner():
    mine()

def notifier():
    notify()

def processor():
    process()

def trader():
    trade()

