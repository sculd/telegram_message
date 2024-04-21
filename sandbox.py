import os, re
import pandas as pd
import publish.telegram

#publish.telegram.send_message("hello world")

import telepot
from pprint import pprint
import time
from telepot.loop import MessageLoop

_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
_chat_id = os.getenv("TELEGRAM_CHAT_ID")

tpbot = telepot.Bot(_bot_token)

pprint(tpbot.getMe())

from telethon import TelegramClient

# Remember to use your own values from my.telegram.org!
api_id = 29272860
api_hash = 'f02e0e26900341c528d949687e850411'
client = TelegramClient('anon', api_id, api_hash)


def extract_symbols(text):
    if text is None:
        return None
    symbols = [w for w in text.split() if '$' in w]
    symbols = [s for s in symbols if re.search('\$[A-Z]+', s) is not None]
    symbols = [re.search('\$[A-Z]+', s).group(0) for s in symbols]
    symbols = [s[1:] for s in symbols if len(s) > 0]
    if len(symbols) == 0:
        return None
    return symbols

def extract_title(text):
    if text is None:
        return None
    text = text.split('**Source')[0]
    text = text.replace('\\n', '\n')
    phrases = text.split('\n')
    phrases = [p.replace('*', '') for p in phrases if '📰🔔' not in p and len(p) > 0]
    return '\n'.join(phrases)

def extract_price_at_news(text):
    if text is None:
        return None
    phrases = text.split('**')
    for i, ph in enumerate(phrases):
        if 'Price at news:' in ph and len(phrases) > i:
            return float(phrases[i+1].strip().strip('$').replace(',', ''))
    return None


async def main():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    timestamps = []
    symbols_list = []
    symbol_list = []
    titles = []
    price_at_news_list = []

    # You can print the message history of any chat:
    async for message in client.iter_messages(-4163187191):
        symbols = extract_symbols(message.text)
        if symbols is None: continue

        title = extract_title(message.text)
        price_at_news = extract_price_at_news(message.text)

        print(f'date: {message.date}, symbols: {symbols}, title: {title}, price_at_news: {price_at_news}')
        for symbol in symbols:
            timestamps.append(message.date)
            symbol_list.append(symbol)
            titles.append(title)
            price_at_news_list.append(price_at_news)

    df = pd.DataFrame.from_dict({'timestamp': timestamps, 'symbol': symbol_list, 'title': titles, 'price_at_new': price_at_news_list})
    df.to_parquet('ambush.parquet')

with client:
    client.loop.run_until_complete(main())
