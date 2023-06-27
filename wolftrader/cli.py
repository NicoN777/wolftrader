"""
    Main point of entry for wolftrade

    To run:
        python cli.py [args]
        "visualize"
        "trade"
"""
import time
import argparse
from wolf import mine, process, notify, trade
from util.logger import log_info


parser = argparse.ArgumentParser(description='CLI to mine, trade, calculate BitCoin',
                                 usage='python cli.py action --frequency=10 (Run action every 10 minutes)\n'
                                       'python cli.py data-mine --frequency=30 (Get prices every 30 minutes)',
                                 add_help=False
                                 )
parser.add_argument('action',
                    type=str,
                    choices=['data-mine', 'data-process', 'notify', 'trade'],
                    help='Select which to run...')
parser.add_argument('-f',
                    '--frequency',
                    type=int,
                    # choices=list(range(15, 1441, 15)),
                    default=10,
                    help='Frequency for action, (run action after every n minutes)')
parser.add_argument('-h', '--help',
                    action='help',
                    help='-f --frequency in minutes, specifies how often to execute\n'
                         'action what you want to run')
args = parser.parse_args()

log_info(f'Started Wolftrader from {__file__}, '
         f'with parameter: {args.action} '
         f'and frequency:  {args.frequency}')

time_in_seconds = args.frequency * 60
try:
    if args.action == 'data-mine':
        while True:
            mine()
            time.sleep(time_in_seconds)
    elif args.action == 'data-process':
        while True:
            process()
            time.sleep(time_in_seconds)
    elif args.action == 'notify':
        while True:
            notify()
            time.sleep(time_in_seconds)
    elif args.action == 'trade':
        while True:
            trade()
            time.sleep(time_in_seconds)
    else:
        print('Parameter not recognized')
except KeyboardInterrupt as e:
    pass
finally:
    log_info(f'Ended Wolftrader from {__file__}, '
             f'with parameter: {args.action} '
             f'and frequency:  {args.frequency}')
