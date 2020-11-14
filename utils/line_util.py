from linebot.models import TextSendMessage, FlexSendMessage, ImageSendMessage
from config.line_bot_api import line_bot_api
import json
from config.main import JST
import datetime
import re


class TextMessageUtil:
    def __init__(self, event):
        self.event = event

    def send_zoom_url(self):
        with open("./config/flex.json") as f:
            flex_json = json.load(f)
        flex_message = FlexSendMessage(
            alt_text='home_room_flex', contents=flex_json["zoom_flex"])
        line_bot_api.reply_message(
            self.event.reply_token, messages=flex_message)

    def send_unit_image(self):
        image_message = ImageSendMessage(
            original_content_url='https://pacific-ocean-18208.herokuapp.com/static/graduation_unit.jpg',
            preview_image_url='https://pacific-ocean-18208.herokuapp.com/static/graduation_unit.jpg'
        )
        line_bot_api.reply_message(
            self.event.reply_token, messages=image_message)

    def text_send_schedule(self):
        message = self.event.message.text
        if message != "schedule":
            split_message = message.split(":")[1]
            if re.fullmatch(r"\d{4}", split_message):
                now_time = datetime.datetime.now(JST).strftime("%Y/") + \
                    f"{split_message[0:2]}/{split_message[2:4]}"
            else:
                return
        else:
            now_time = datetime.datetime.now(JST).strftime("%Y/%m/%d")
        now_time_split = now_time.split("/")
        now_time_text = f"{now_time_split[1]}月{now_time_split[2]}日"
        send_text = f"{now_time_text}の時間割"
        with open("./config/schedule.json") as f:
            schedule_json = json.load(f)
        for v in schedule_json.values():
            if v['day'] == now_time:
                send_text += f"\n\n{v['time_table']}時間目\n{v['class_name']}\nPASS : {v['class_room_password']}\nhttps://zoom.us/j/{v['class_room_number']}?"
        if send_text == f"{now_time_text}の時間割":
            line_bot_api.reply_message(
                self.event.reply_token, TextSendMessage(text=f"申し訳ありません。\n{now_time_text}の時間割が存在しません。"))
        else:
            line_bot_api.reply_message(
                self.event.reply_token, TextSendMessage(text=send_text))

    def send_test(self):
        line_bot_api.reply_message(
            self.event.reply_token, TextSendMessage(text="test"))

    def send_help(self):
        with open("./config/help.txt") as f:
            help_txt = f.read()
        line_bot_api.reply_message(
            self.event.reply_token, TextSendMessage(text=help_txt))

    def send_schedule(self):
        message = self.event.message.text
        if ":" in message:
            split_message = message.split(":")[1]
            if re.fullmatch(r"\d{4}", split_message):
                now_time = datetime.datetime.now(JST).strftime("%Y/") + \
                    f"{split_message[0:2]}/{split_message[2:4]}"
            else:
                return
        else:
            now_time = datetime.datetime.now(JST).strftime("%Y/%m/%d")
        now_time_split = now_time.split("/")
        with open("./config/schedule.json") as f:
            schedule_json = json.load(f)
        limit_count = 0
        classroom_num = 0
        messages = []
        add_flex = {
            "type": "carousel",
            "contents": []
        }
        for v in schedule_json.values():
            if v['day'] == now_time:
                class_name = v['class_name'].replace(
                    "イノベーションプロジェクト", "イノプロ").replace("英語コア・スキルズ", "コアスキルズ")
                classroom_num += 1
                add_json = {
                    "type": "bubble",
                    "size": "micro",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{v['time_table']}時間目",
                                "weight": "bold",
                                "size": "sm",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": class_name,
                                "weight": "bold",
                                "size": "sm",
                                "wrap": False
                            },
                            {
                                "type": "text",
                                "text": f"ID : {v['class_room_number']}",
                                "weight": "bold",
                                "size": "sm",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": f"PASS : {v['class_room_password']}",
                                "weight": "bold",
                                "size": "sm",
                                "wrap": True
                            },

                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "ここをタップ",
                                    "uri": f"https://zoom.us/j/{v['class_room_number']}?"
                                }
                            }
                        ]
                    }
                }
                if 10 == limit_count:
                    limit_count = 0
                    messages.append(FlexSendMessage(
                        alt_text='home_room_flex', contents=add_flex))
                    add_flex = {
                        "type": "carousel",
                        "contents": []
                    }
                add_flex["contents"].append(add_json)
                limit_count += 1
        if limit_count != 0:
            messages.append(FlexSendMessage(
                alt_text='home_room_flex', contents=add_flex))
        if classroom_num != 0:
            text_send_message = TextSendMessage(
                text=f"{now_time_split[1]}月{now_time_split[2]}日の時間割")
        else:
            text_send_message = TextSendMessage(
                text=f"申し訳ありません。\n{now_time_split[1]}月{now_time_split[2]}日の時間割が存在しません。")
        messages.insert(0, text_send_message)
        line_bot_api.reply_message(
            self.event.reply_token, messages=messages)

    def send_schedule_e(self):
        message = self.event.message.text
        get_number = re.compile('[a-z]+').findall(message)
        if not get_number:
            line_bot_api.reply_message(
                self.event.reply_token, TextSendMessage(
                    text="クラスを入力してください。"))
            return
        class_number = get_number[0].lower()
        print(class_number)
        now_time = datetime.datetime.now(JST)
        print(now_time.weekday())
        with open("./config/schedule_e.json") as f:
            schedule_json = json.load(f)
        limit_count = 0
        classroom_num = 0
        messages = []
        add_flex = {
            "type": "carousel",
            "contents": []
        }
        for v in schedule_json["data"]:
            if v['class_number'] == class_number and v['day_of_week'] == now_time.weekday():
                print("ssssss")
                class_name = v['class_name']
                classroom_num += 1
                add_json = {
                    "type": "bubble",
                    "size": "micro",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{v['time_table']}時間目",
                                "weight": "bold",
                                "size": "sm",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": class_name,
                                "weight": "bold",
                                "size": "sm",
                                "wrap": False
                            },
                            {
                                "type": "text",
                                "text": f"ID : {v['class_room_number']}",
                                "weight": "bold",
                                "size": "sm",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": f"PASS : {v['class_room_password']}",
                                "weight": "bold",
                                "size": "sm",
                                "wrap": True
                            },

                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "ここをタップ",
                                    "uri": f"https://zoom.us/j/{v['class_room_number']}?"
                                }
                            }
                        ]
                    }
                }
                add_flex["contents"].append(add_json)
                limit_count += 1
        if limit_count != 0:
            messages.append(FlexSendMessage(
                alt_text='home_room_flex', contents=add_flex))
        if classroom_num != 0:
            text_send_message = TextSendMessage(
                text=f"{class_number}組の今日の時間割はこちらです。")
        else:
            text_send_message = TextSendMessage(
                text="申し訳ありません。\n今日の時間割が存在しません。")
        messages.insert(0, text_send_message)
        line_bot_api.reply_message(
            self.event.reply_token, messages=messages)
