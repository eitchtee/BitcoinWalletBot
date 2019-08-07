from random import choice

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, Filters, CallbackQueryHandler)
from telegram.ext.dispatcher import run_async
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID, BITCOIN_WALLET, MONEY,\
    MONEY_FORMAT

from api import final_balance, convert_to_money, get_txs

from money.money import Money


def buttons(tipo: str = 'main'):
    keyboard = []
    if tipo == 'main':
        keyboard = [
            [InlineKeyboardButton('Transactions', callback_data='transactions'),
             InlineKeyboardButton('🔄', callback_data='update'), ],
        ]

    elif tipo == 'tx':
        keyboard = [
            [InlineKeyboardButton('⬅️ Return', callback_data='update')],
        ]

    elif tipo == 'no_input':
        keyboard = [
            [InlineKeyboardButton('🔄', callback_data='update'), ],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


def gui_text():
    balance, balance_not_confirmed = final_balance(BITCOIN_WALLET)
    soma_saldos = balance + balance_not_confirmed
    balance_money, btc_value = convert_to_money(soma_saldos)

    balance_money_fmtd = Money(str(balance_money), MONEY).format(
        MONEY_FORMAT)
    btc_value_fmtd = Money(str(btc_value), MONEY).format(MONEY_FORMAT)

    txt = '*Bitcoin Wallet Viewer*\n\n' \
          '💰 *{}* confirmed btc.\n' \
          '💸 *{}* non confirmed btc.\n' \
          '💱 *{}* in total.\n\n' \
          '📈 *1BTC* currently is worth *{}*'.format(balance,
                                                    balance_not_confirmed,
                                                    str(balance_money_fmtd),
                                                    str(btc_value_fmtd))

    return txt


def tx_history(wallet: str):
    txs_list = get_txs(wallet)

    if txs_list:
        del txs_list[9:]
        result = ['*Transactions*\n']
        for tx in txs_list:
            pretty_tx = '📅 {}\n💰 {} btc\n'.format(tx[0], tx[1])
            result.append(pretty_tx)

        return '\n'.join(result)
    else:
        return '_No transactions to show._'


def start(bot, update):
    # Send the message with menu
    update.message.reply_text(gui_text(),
                              reply_markup=buttons(),
                              parse_mode='Markdown')


@run_async
def answer_handler(bot, update):
    query = update.callback_query.data

    possible_texts = ['Updating..._',
                      'Updating.._',
                      'Updating...._',
                      '_Retrieving information.._',
                      '_Retrieving information..._',
                      '_Retrieving information...._']

    if query == 'update':
        bot.edit_message_text(
            text=choice(possible_texts),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=buttons('no_input'),
            parse_mode='Markdown')

        bot.edit_message_text(
            text=gui_text(),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=buttons(),
            parse_mode='Markdown')

    elif query == 'transactions':
        bot.edit_message_text(
            text=choice(possible_texts),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=buttons('no_input'),
            parse_mode='Markdown')

        bot.edit_message_text(
            text=tx_history(BITCOIN_WALLET),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=buttons('tx'),
            parse_mode='Markdown')


# @run_async
def error(bot, update, erro):
    print('Update "{}" caused error "{}"'.format(update, erro))


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)

    updater.dispatcher.add_handler(
        CommandHandler('start', start, Filters.user(TELEGRAM_USER_ID)))
    updater.dispatcher.add_handler(CallbackQueryHandler(answer_handler))
    updater.dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
