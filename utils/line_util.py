from linebot.models import ImageSendMessage
from config.line_bot_api import line_bot_api, heroku_url, num_list
import re


class TextMessageUtil:
    def __init__(self, event):
        self.event = event

    def send_pass_image(self):
        num = re.sub("\\D", "", self.event.message.text)
        if int(num) not in num_list:
            return
        image_url = f'{heroku_url}/static/{num}.png'
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        line_bot_api.reply_message(
            self.event.reply_token, messages=image_message)
