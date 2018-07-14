#Author: Nicolas Nunez
#Put my fucking data in lovely csv format

import csv
import json
import pandas as pd
import datetime

with open('data/spot_price.json', 'r') as spot, \
        open('data/sell_price.json', 'r') as sell, \
        open('data/buy_price.json', 'r') as buy, \
        open('data/timestamps.json') as timestamps:

    records = list()
    for a,b,c,d in zip(timestamps, buy, spot, sell):
        records.append((json.loads(a),json.loads(b),json.loads(c),json.loads(d)))

price_record = {'EXTRACTION_DATE': list(),
                'BUY_PRICE': list(),
                'BUY_PRICE_CURRENCY': list(),
                'SPOT_PRICE': list(),
                'SPOT_PRICE_CURRENCY': list(),
                'SELL_PRICE': list(),
                'SELL_PRICE_CURRENCY': list()}
for record in records:
    i = 0
    for data in record:
        if 'data' in data.keys():
            if 'iso' in data['data'].keys():
                i += 1
                date = data['data']['iso']
                price_record['EXTRACTION_DATE'].append(date)
            else:
                i += 1
                base = data['data']['base']
                currency = data['data']['currency']
                amount = data['data']['amount']
                if i == 2:
                    price_record['BUY_PRICE'].append(amount)
                    price_record['BUY_PRICE_CURRENCY'].append(currency)
                if i == 3:
                    price_record['SPOT_PRICE'].append(amount)
                    price_record['SPOT_PRICE_CURRENCY'].append(currency)
                if i == 4:
                    price_record['SELL_PRICE'].append(amount)
                    price_record['SELL_PRICE_CURRENCY'].append(currency)

records = pd.DataFrame(price_record)
records[['EXTRACTION_DATE', 'BUY_PRICE', 'BUY_PRICE_CURRENCY', 'SPOT_PRICE', 'SPOT_PRICE_CURRENCY', 'SELL_PRICE', 'SELL_PRICE_CURRENCY']].to_csv('db/raw_prices.csv', header=False, index=False)
