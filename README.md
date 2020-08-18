<div align="center">
    <img alt="BitcoinWalletBot Example" title="BitcoinWalletBot" src="./.github/images/header.png" />
</div>

<h3 align="center">BitcoinWalletBot</h3>
<p align="center">A Telegram Bot to check your bitcoin wallet.</p>

---

<p align="center">
    <a href="#getting-started">Getting Started</a> |
    <a href="#configuration">Configuration</a> |
    <a href="#contributing">Contributing</a> |
    <a href="#license">License</a>
</p>

---

## Getting Started
1. Clone this repo
2. Install requirements: ``pip install -r requirements.txt``
3. Run bot: ``python bot.py``

## Configuration
#### configs.yml
BitcoinWalletBot uses a ``configs.yml`` file on the same folder as ``bot.py`` for configurations.

```yaml
# Avaliable as a tag
bot_title: "Bitcoin Wallet Viewer"

# Telegram bot token as provided by BotFather
telegram_token : ''
# A list of ints composed of all Telegram user ids
# you want to be able to use the bot
allowed_user_ids:
  - 1234567

update_each: 3600 # seconds
date_format: "%d/%m/%Y" # datetime compliant format
hour_format": "%H:%M" # datetime compliant format

money: "USD"
money_format: "en_US"

wallets:
  - name: Test Wallet
    address: "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"
  - name: Test Wallet
    address: "aaa1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"

# BOT STRINGS ---------------------------------------------
# Each new item is joined by a new line, use \n if you need extra spacing

title:
  - "*{title}*"
wallet_view:
  - "\n\n*- {wallet}*"
  - "💰 *{btc_balance}* BTC"
  - "💱 *{money_balance}* in {currency}"
failed_wallet_view:
  - "\n\n*- {wallet}*"
  - "_Unable to fetch wallet information._"
extra_content:
  - "\n\n\n📈 *1BTC* is worth *{btc_value}*"
  - "\n_🕗 Last update: {update_date} at {update_time}_"
update_button: "🔄"

updating:
  - "_Updating.._"
  - "_Updating..._"
  - "_Fetching information.._"
  - "_Fetching information..._"
  - "_Retrieving information.._"
  - "_Retrieving information..._"
```

#### Tags
When you are updating your strings, you can use some tags to display specific information. They are:


- ``{title}``: bot title as specified on your config.json
- ``{update_date}``: date
- ``{update_time}``: time
- ``{btc_value}``: the current value of 1 BTC
- ``{currency}``: the currency code you specified (e.g. ``USD``)


#### ``wallet_view`` tags
These tags are only avaliable to use when editing the wallet_view section. They are:

- ``{btc_balance}``: the balance in BTC of the wallet
- ``{money_balance}``: the balance of the wallet in currency
- ``{wallet}``: the name of the wallet. This is also avaliable on the wallet_view_falied section
- ``{wallet_address}``: the address of the wallet. This is also avaliable on the wallet_view_falied section


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)