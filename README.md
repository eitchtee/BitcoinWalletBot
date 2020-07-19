# BitcoinWalletBot
A Telegram Bot to check your bitcoin wallets.

---

## Configs
### configs.json
```json
{
  "bot": {
    "title": "", // The title for your bot, down below you can choose to use it or not
    "telegram_token": "", // The bot token as provided by botfather on telegram
    "allowed_user_ids": [123, 456], // User ids you want to access the bot. Usually is only yours
    "update_each": 3600, // Amount of seconds to wait before automatically updating the data. Leave as 0 to disable
    "date_format": "%d/%m/%Y", // Date format for use down below
    "hour_format": "%H:%M" // Time format for use down below
  },

  "money": {
    "currency": "USD", // Code for the currency you want to see exchange details
    "currency_format": "en_US" // Coutries have different ways of handling money formats, you can change that here
  },

  "wallets": [{
    "name": "Test Wallet", // The name of the wallet
    "address": "" // Wallet address
  }],

// This should be self-explanatory
  "strings": {
    "title": ["*{title}*", "", ""],
    "wallet_view": ["*{wallet}*",
    "\uD83D\uDCB0 *{btc_balance}* BTC.",
      "\uD83D\uDCB1 *{money_balance}* in {currency}."],
    "failed_wallet_view": ["*{wallet}*",
      "_Unable to fetch information about this wallet._"],
    "extra_content": ["","",
      "\uD83D\uDCC8 *1BTC* is worth *{btc_value}*",
      "", "",
      "_\uD83D\uDD57 Last update: {update_date} at {update_time}_"],
    "update_strings": ["Updating..",
      "Updating...",
      "Fetching information..",
      "Fetching information...",
      "_Retrieving information.._",
      "_Retrieving information..._"
    ],
    "update_button": "\uD83D\uDD04"
  }
}
```

### tags
When you are updating your strings, you can use some tags to display specific information. They are:

```
{title}: bot title as specified on your config.json
{update_date}: date
{update_time}: time
{btc_value}: the current value of 1 BTC
{currency}: the currency code you specified on the money part of the json
```

### "wallet_view" tags
These tags are only avaliable to use when editing the wallet_view section. They are:

```
{btc_balance}: the balance in BTC of the wallet
{money_balance}: the balance of the wallet in currency
{wallet}: the name of the wallet. This is also avaliable on the wallet_view_falied section
{wallet_address}: the address of the wallet. This is also avaliable on the wallet_view_falied section
```

##### For now configurations are not sanitized or checked before running and will break your bot if not correctly set.
##### Create an issue if you find any problems.