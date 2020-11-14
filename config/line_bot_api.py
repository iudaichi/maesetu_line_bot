from datetime import timedelta, timezone
import os
from linebot import LineBotApi, WebhookHandler


LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


JST = timezone(timedelta(hours=+9), 'JST')
heroku_url = "https://maesetu-line-bot.herokuapp.com"
num_list = [200016, 617859, 876184, 471227]
