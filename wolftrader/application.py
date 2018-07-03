import configparser
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))
WOLF = os.path.join(PROJECT_ROOT, os.path.join(os.path.abspath(os.path.dirname(__file__))))

try:
    config=configparser.RawConfigParser()
    config.read(os.path.join(WOLF, 'resources/conf', 'application.properties'))
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

    #HtmlTemplates
    email_buy_template = os.path.join(WOLF, config.get('HtmlTemplates', 'email.template.buy'))
    email_sell_template = os.path.join(WOLF, config.get('HtmlTemplates','email.template.sell'))
    email_report_template = os.path.join(WOLF, config.get('HtmlTemplates','email.template.report'))

    #Reports
    report_buy = os.path.join(WOLF, config.get('Reports','report.buy'))
    report_sell = os.path.join(WOLF, config.get('Reports','report.sell'))
    report_report = os.path.join(WOLF, config.get('Reports','report.report'))

    #Images
    wolf_logo = os.path.join(WOLF, config.get('Images', 'wolfie.logo.img'))
except Exception as error:
    print('An error has occurred: {}'.format(error.error))
