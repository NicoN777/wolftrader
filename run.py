"""
    Main point of entry for wolftrade

    To run:
        python run.py [args]
        "mine"
        "visualize"
        "trade"
"""
import sys
import time

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'data_mine':
            while True:
                from wolftrader.wolf import mine
                mine()
                time.sleep(300)
        elif sys.argv[1] == 'data_process':
            while True:
                from wolftrader.wolf import process
                process()
                time.sleep(300)
        elif sys.argv[1] == 'notify':
            while True:
                from wolftrader.wolf import notify
                notify()
                time.sleep(3600)
        elif sys.argv[1] == 'trade':
            while True:
                from wolftrader.wolf import trade
                trade()
                time.sleep(300)
        else:
            print('Parameter not recognized')
    else:
        print ("The fuck you talkin 'bout playa")



