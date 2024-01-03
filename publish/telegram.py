import os, requests

_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
_chat_id = os.getenv("TELEGRAM_CHAT_ID")

def send_message(message):
    url = f"https://api.telegram.org/bot{_bot_token}/sendMessage?chat_id={_chat_id}&text={message}"
    print(requests.get(url).json())
