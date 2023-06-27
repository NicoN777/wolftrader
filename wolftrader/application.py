import configparser
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))
WOLF = os.path.join(PROJECT_ROOT, os.path.join(os.path.abspath(os.path.dirname(__file__))))

try:
    config=configparser.RawConfigParser()
    config.read(os.path.join(WOLF, 'resources/conf', 'wolfie.ini'))

    #Database Properties
    database_name = os.path.join(PROJECT_ROOT, config.get('DatabaseProperties', 'database.name'))
    database_username = str(config.get('DatabaseProperties', 'database.username'))
    database_password = str(config.get('DatabaseProperties', 'database.password'))
    database_settings = str(config.get('DatabaseProperties', 'database.settings'))

    #Log Properties
    log_file = os.path.join(PROJECT_ROOT, config.get('LogProperties', 'log.file'))
    log_level = config.getint('LogProperties', 'log.level')
    log_format = str(config.get('LogProperties', 'log.format'))

    #Coinbase Properties
    coinbase_user_key = str(config.get('CoinbaseProperties', 'coinbase.user.key'))
    coinbase_user_secret = str(config.get('CoinbaseProperties', 'coinbase.user.secret'))

    #Email Properties
    gmail_account = str(config.get('EmailProperties', 'gmail.account'))
    gmail_password = str(config.get('EmailProperties', 'gmail.pass'))
    gmail_port = config.getint('EmailProperties', 'gmail.port')
    gmail_stmp = str(config.get('EmailProperties', 'gmail.smtp'))
    mail_recipients = str(config.get('EmailProperties', 'mail.recipients')).split(',')

    #HtmlTemplates
    email_buy_template = os.path.join(WOLF, config.get('HtmlTemplates', 'email.template.buy'))
    email_sell_template = os.path.join(WOLF, config.get('HtmlTemplates','email.template.sell'))
    email_report_template = os.path.join(WOLF, config.get('HtmlTemplates','email.template.report'))

    #Reports
    report_buy = os.path.join(WOLF, config.get('Reports','report.buy'))
    report_sell = os.path.join(WOLF, config.get('Reports','report.sell'))
    report_report = os.path.join(WOLF, config.get('Reports','report.report'))
    report_table = os.path.join(WOLF, config.get('Reports', 'report.report.table'))
    indicators_csv = os.path.join(WOLF, config.get('Reports', 'report.csv'))

    #Images
    wolf_logo = os.path.join(WOLF, config.get('Images', 'image.logo.wolfie'))
    indicators_graph = os.path.join(WOLF, config.get('Images', 'image.graph.indicators'))
    rsi_graph = os.path.join(WOLF, config.get('Images', 'image.graph.rsi'))

    #Twilio
    twilio_sid =  config.get('Twilio', 'sid')
    twilio_token = config.get('Twilio', 'token')
    sms_recipients = str(config.get('Twilio', 'sms.recipients')).split(',')
    sender = config.get('Twilio', 'sender')

    #AzureSQLDatabase

    __azure_server = config.get('AzureSQLDatabase', 'server')
    __azure_database = config.get('AzureSQLDatabase', 'database')
    __azure_username = config.get('AzureSQLDatabase', 'username')
    __azure_password = config.get('AzureSQLDatabase', 'password')
    __azure_port = config.getint('AzureSQLDatabase', 'port')
    __azure_driver = config.get('AzureSQLDatabase', 'driver')
    azure_connection_string = 'DRIVER='+__azure_driver+';SERVER='+__azure_server\
                              +';PORT=1443;DATABASE='+__azure_database\
                              +';UID='+__azure_username+';PWD='+ __azure_password

    #Azure FileStore
    azure_store_account_name = config.get('AzureFileStore', 'account.name')
    azure_store_connstr = config.get('AzureFileStore', 'connection.string')

except Exception as error:
    print('An error has occurred: {}'.format(error.error))
