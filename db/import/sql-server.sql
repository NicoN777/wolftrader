BULK INSERT dbo.price_history FROM 'price_history.csv' WITH (FIRSTROW = 2, FIELDTERMINATOR = ',',ROWTERMINATOR = '\n') GO

BULK INSERT dbo.indicators
FROM 'indicators.csv'
WITH
(
FIRSTROW = 2,
FIELDTERMINATOR = ',',
ROWTERMINATOR = '\n'
)
GO

BULK INSERT dbo.users
FROM 'users.csv'
WITH
(
FIRSTROW = 2,
FIELDTERMINATOR = ',',
ROWTERMINATOR = '\n'
)
GO

BULK INSERT dbo.buy_history
FROM 'buy_history.csv'
WITH
(
FIRSTROW = 2,
FIELDTERMINATOR = ',',
ROWTERMINATOR = '\n'
)
GO

BULK INSERT dbo.sell_history
FROM 'sell_history.csv'
WITH
(
FIRSTROW = 2,
FIELDTERMINATOR = ',',
ROWTERMINATOR = '\n'
)
GO