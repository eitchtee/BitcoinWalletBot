import requests
from datetime import datetime, timezone
from config import CURRENCY


def final_balance(wallet: str, btc: bool = True):
    api_link = "https://blockchain.info/rawaddr/"

    request = requests.get(api_link + wallet)
    satoshi_confirmed = int(request.json()['final_balance'])

    btc_confirmed = satoshi_confirmed / 100000000

    api_link = 'https://www.blockonomics.co/api/balance'
    payload = {"addr": wallet}

    result = requests.post(api_link, json=payload).json()

    satoshi_not_confirmed = result['response'][0]['unconfirmed']
    btc_not_confirmed = satoshi_not_confirmed / 100000000

    if btc:
        return btc_confirmed, btc_not_confirmed
    else:
        return satoshi_confirmed, satoshi_not_confirmed


def convert_to_money(value, currency: str = CURRENCY):
    api_link = "https://blockchain.info/ticker"

    request = requests.get(api_link)
    result_list = request.json()
    btc_value = result_list[currency]["15m"]

    final_value = round(value * btc_value, 2)

    return final_value, btc_value


def get_txs(wallet: str):
    api_link = "https://www.blockonomics.co/api/searchhistory"

    payload = {"addr": wallet}

    result = requests.post(api_link, json=payload).json()

    tx_history = []
    for tx in result['history']:
        date = tx['time']
        date = datetime.utcfromtimestamp(date).replace(
            tzinfo=timezone.utc).astimezone(tz=None).strftime('%d/%m/%Y %H:%M')
        value = tx['value']
        value = value / 100000000
        tx_history.append([date, value])

    return tx_history
