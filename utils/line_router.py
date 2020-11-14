from utils.line_util import TextMessageUtil


class TextMessageRouter:
    def __init__(self, event):
        self.event = event

    def distribution_message(self):
        message = self.event.message.text
        if message.startswith('pa'):
            TextMessageUtil(self.event).send_pass_image()
