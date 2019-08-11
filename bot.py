from random import choice
import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, Filters, CallbackQueryHandler)
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID, BITCOIN_WALLET, MONEY,\
    MONEY_FORMAT

from api import final_balance, convert_to_money, get_txs

from money.money import Money


def bitcoin_refresh_handler(bot, job):
    menu = job.context
    msg = gui_text()
    bot.edit_message_text(
        text=msg,
        chat_id=menu.chat.id,
        message_id=menu.message_id,
        reply_markup=buttons(),
        parse_mode='Markdown')


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

    updated_at = datetime.datetime.now().strftime('%d/%m/%Y at %H:%M')

    txt = '*Bitcoin Wallet Viewer*\n\n' \
          '💰 *{}* confirmed btc.\n' \
          '💸 *{}* non confirmed btc.\n' \
          '💱 *{}* in total.\n\n' \
          '📈 *1BTC* currently is worth *{}*\n\n\n\n' \
          '_🕗 Updated on {}_'.format(balance,
                                     balance_not_confirmed,
                                     str(balance_money_fmtd),
                                     str(btc_value_fmtd),
                                     updated_at)

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


def start(bot, update, job_queue):
    # Send the message with menu
    menu = update.message.reply_text(gui_text(),
                                     reply_markup=buttons(),
                                     parse_mode='Markdown')
    # Updates the display every 15 minutes
    if len(job_queue.jobs()) < 1:
        job_queue.run_repeating(
            bitcoin_refresh_handler, 900, first=60, context=menu)


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


def error(bot, update, erro):
    print('Update "{}" caused error "{}"'.format(update, erro))


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)

    updater.dispatcher.add_handler(
        CommandHandler('start', start, Filters.user(TELEGRAM_USER_ID),
                       pass_job_queue=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(answer_handler))
    updater.dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
