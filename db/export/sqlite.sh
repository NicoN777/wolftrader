sqlite3 -header -csv ../Coinbase.db "select * from price_history;" > price_history.csv
sqlite3 -header -csv ../Coinbase.db "select * from buy_history;" > buy_history.csv
sqlite3 -header -csv ../Coinbase.db "select * from sell_history;" > sell_history.csv
sqlite3 -header -csv ../Coinbase.db "select * from indicators;" > indicators.csv
sqlite3 -header -csv ../Coinbase.db "select * from users;" > users.csv