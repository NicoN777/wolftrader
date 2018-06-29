"""
    Main point of entry for wolftrade

    To run:
        python run.py [args]
        "mine"
        "visualize"
        "trade"
"""
import sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'data_mine':
            from wolftrader.wolf import mine
            mine()
        elif sys.argv[1] == 'data_visualize':
            from wolftrader.wolf import visualize
            visualize()
        elif sys.argv[1] == 'trade':
            from wolftrader.wolf import trade
            trade()
        else:
            print('Parameter not recognized')
    else:
        print ("The fuck you talkin 'bout playa")



