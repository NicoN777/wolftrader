CREATE TABLE PRICE_HISTORY
(
EXTRACTION_DATE datetime PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
BUY_PRICE FLOAT,
BUY_PRICE_CURRENCY VARCHAR(6),
SPOT_PRICE FLOAT,
SPOT_PRICE_CURRENCY VARCHAR(6),
SELL_PRICE FLOAT,
SELL_PRICE_CURRENCY VARCHAR(6)
);

CREATE TABLE INDICATORS
(
CALCULATION_DATE datetime PRIMARY KEY DEFAULT CURRENT_TIMESTAMP),
SPOT_PRICE FLOAT,
BUY_PRICE FLOAT,
SELL_PRICE FLOAT,
MA24 FLOAT,
UPPER_BOLLINGER FLOAT,
LOWER_BOLLINGER FLOAT,
AVG_GAIN FLOAT,
AVG_LOSS FLOAT,
RSI FLOAT
);

CREATE TABLE USERS
(
ID VARCHAR(50) PRIMARY KEY,
NAME VARCHAR(40),
EMAIL VARCHAR(40),
USERNAME VARCHAR(40)
);

CREATE TABLE BUY_HISTORY
(
BUY_ID VARCHAR(50) PRIMARY KEY,
BUY_DATE datetime DEFAULT CURRENT_TIMESTAMP,
BUY_AMOUNT FLOAT,
BUY_PRICE FLOAT,
BUY_PRICE_CURRENCY VARCHAR(20),
BUY_FEE FLOAT,
BUY_TOTAL_PRICE FLOAT
);

CREATE TABLE SELL_HISTORY
(
SELL_ID VARCHAR(50) PRIMARY KEY,
SELL_DATE DATE DEFAULT CURRENT_TIMESTAMP,
SELL_AMOUNT FLOAT,
SELL_PRICE FLOAT,
SELL_PRICE_CURRENCY VARCHAR(20),
TOTAL_SALE_PRICE FLOAT,
GAIN_LOSS_PERCENT FLOAT -- (SELL_PRICE /BUY_PRICE)-1
);