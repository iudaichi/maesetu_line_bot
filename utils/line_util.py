from linebot.models import ImageSendMessage, TextSendMessage
from config.line_bot_api import line_bot_api, heroku_url, num_list
import re


class TextMessageUtil:
    def __init__(self, event):
        self.event = event

    def send_pass_image(self):
        num = re.sub("\\D", "", self.event.message.text)
        if int(num) not in num_list:
            return
        image_url = f'{heroku_url}/static/{num}.jpg'
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        announce_message = TextSendMessage(
            text="はしれ！まえせつをプレイしてくれてありがとう！\n\n今回の特典写真はこちら！")
        thx_message = TextSendMessage(
            text="ほかにも様々な特典が隠されているので引き続きプレイしてゲットしよう！")
        messages = [announce_message, image_message, thx_message]
        line_bot_api.reply_message(
            self.event.reply_token, messages=messages)
