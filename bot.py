from random import choice
import datetime
import json
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, Filters,
                          CallbackQueryHandler)

from api import final_balance, convert_to_money

from money.money import Money
from money.currency import Currency

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %('
                           'message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_configs():
    # Reading the file everytime allows for changes while the bot is running
    with open("configs.json", 'r') as f:
        configs = json.load(f)
    return configs


def start(update, context):
    configs = get_configs()
    update_delay = configs["bot"]["update_each"]

    # Send the message with menu
    menu = update.message.reply_text(gui_text(),
                                     reply_markup=buttons(),
                                     parse_mode='Markdown')

    # Updates the display every x minutes
    if len(context.job_queue.jobs()) < 1 and update_delay > 0:
        context.job_queue.run_repeating(bitcoin_refresh_handler,
                                        update_delay,
                                        first=update_delay,
                                        context=menu)


def bitcoin_refresh_handler(context):
    menu = context.job.context
    updating_txt = get_configs()["strings"]["update_strings"]

    context.bot.edit_message_text(
        text=choice(updating_txt),
        chat_id=menu.chat.id,
        message_id=menu.message_id,
        reply_markup=buttons("no_input"),
        parse_mode='Markdown')

    context.bot.edit_message_text(
        text=gui_text(),
        chat_id=menu.chat.id,
        message_id=menu.message_id,
        reply_markup=buttons(),
        parse_mode='Markdown')


def gui_text():
    configs = get_configs()
    bot_configs = configs["bot"]
    wallets = configs["wallets"]
    money_configs = configs["money"]
    strings = configs["strings"]

    bot_title = bot_configs["title"]

    currency_txt = money_configs["currency"]
    currency = getattr(Currency, currency_txt)
    money_format = money_configs["currency_format"]

    update_date = datetime.datetime.now().strftime(bot_configs["date_format"])
    update_hour = datetime.datetime.now().strftime(bot_configs["hour_format"])

    placeholder, one_btc_value = convert_to_money(1, currency_txt)
    one_btc_value_frmt = Money(str(one_btc_value), currency). \
        format(money_format)

    start_replacements = {"title": bot_title,
                          "update_date": update_date,
                          "update_time": update_hour,
                          "btc_value": one_btc_value_frmt,
                          "currency": currency_txt}

    txt = ["\n".join(strings["title"]).format(**start_replacements)]

    for wallet in wallets:
        wallet_name = wallet["name"]
        wallet_addr = wallet['address']
        balance_btc = final_balance(wallet_addr)
        if balance_btc is not None:
            balance_money, btc_value = convert_to_money(balance_btc,
                                                        currency_txt)
            balance_money = Money(str(balance_money),
                                  currency).format(money_format)

            wallet_replacements = {"btc_balance": balance_btc,
                                   "money_balance": balance_money,
                                   "wallet": wallet_name,
                                   "wallet_address": wallet_addr}

            txt.append("\n".join(strings["wallet_view"]).
                       format(**wallet_replacements, **start_replacements))
        else:
            wallet_replacements = {"wallet": wallet_name,
                                   "wallet_address": wallet_addr}

            txt.append("\n".join(strings["wallet_view"]).
                       format(**wallet_replacements, **start_replacements))

    txt.append("\n".join(strings["extra_content"]).format(**start_replacements))

    return ''.join(txt)


def buttons(tipo: str = 'main'):
    configs = get_configs()
    strings = configs["strings"]

    keyboard = []
    if tipo == 'main':
        keyboard = [
            [InlineKeyboardButton(strings["update_button"],
                                  callback_data='update'), ],
        ]

    elif tipo == 'no_input':
        keyboard = [
            [InlineKeyboardButton(strings["update_button"],
                                  callback_data='update'), ],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


def answer_handler(update, context):
    query = update.callback_query.data

    configs = get_configs()
    updating_texts = configs["strings"]["update_strings"]

    if query == 'update':
        context.bot.edit_message_text(
            text=choice(updating_texts),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=buttons('no_input'),
            parse_mode='Markdown')

        context.bot.edit_message_text(
            text=gui_text(),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=buttons(),
            parse_mode='Markdown')


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    configs = get_configs()

    updater = Updater(configs["bot"]["telegram_token"], use_context=True)

    updater.dispatcher.add_handler(
        CommandHandler('start', start,
                       Filters.user(configs["bot"]["allowed_user_ids"])))
    updater.dispatcher.add_handler(CallbackQueryHandler(answer_handler))
    updater.dispatcher.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
