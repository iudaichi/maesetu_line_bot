from linebot.models import ImageSendMessage
from config.line_bot_api import line_bot_api, heroku_url


class TextMessageUtil:
    def __init__(self, event):
        self.event = event

    def send_pass_image(self):
        image_message = ImageSendMessage(
            original_content_url=f'{heroku_url}/static/logo.jpg',
            preview_image_url=f'{heroku_url}/static/logo.jpg'
        )
        line_bot_api.reply_message(
            self.event.reply_token, messages=image_message)
