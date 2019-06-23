from money.currency import Currency


TELEGRAM_BOT_TOKEN = ''  # [str] telegram bot token, get this from BotFather
TELEGRAM_USER_ID = 123  # [int] | list([int]) will only allow commands from these ids
BITCOIN_WALLET = ''  # [str] your bitcoin wallet hash

# all of these configs needs to be for the same currency
CURRENCY = 'USD'  # [str] your currency code
MONEY = Currency.USD  # [Currency class] from py-money, just change the end
MONEY_FORMAT = 'en_US'  # [str] contry code (e.g. en_US, pt_BR...)
