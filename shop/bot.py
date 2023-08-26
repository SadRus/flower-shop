import telegram


class TelegramNotifier():
    def __init__(self, token, chat_id):
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=token)

    def send_notify(self, message):
        self.tg_bot.send_message(chat_id=self.chat_id, text=message)
