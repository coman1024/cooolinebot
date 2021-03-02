# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import os
import sys
import re

from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    PostbackEvent,
    TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    FlexSendMessage,
    MessageTemplateAction
)


from menu import (
    featureMenu,
    rewMenu,
    saveMenu,
    notifyMenu,
    shiftMenu
)
from menu.featureMenu import(
    menu1,
    menu3
)


from clock import Scheduler

from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
print("sio start app !!")
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

defaultText = "查無指令"

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('cron', day_of_week='tue,fri', hour='22', minute='10', timezone='Asia/Taipei')
def lottery649_drawing_job():
    print("開始通知")
    subscriber_ids = notifyMenu.getIdAll()
    if (len(subscriber_ids) == 0):
        print("沒有通知")
        return "OK"

    for id in subscriber_ids:
        try:
            line_bot_api.push_message(id[0],  FlexSendMessage(
                alt_text = "最新中獎號碼",
                contents = rewMenu.newestReward()
            ))
        except Exception:
            continue        

@scheduler.scheduled_job('cron', day='20', hour='10', minute='30', timezone='Asia/Taipei')
def pickLotteryNumber_job():
    print("誰去買樂透")
    subscriber_ids = notifyMenu.getIdAll()
    if (len(subscriber_ids) == 0):
        print("沒有通知")
        return "OK"

    for id in subscriber_ids:
        try:
            line_bot_api.push_message(id[0],  FlexSendMessage(
                    alt_text = "誰去買樂透",
                    contents = shiftMenu.shift()
                ))
        except Exception as e:
            print(str(e))
            continue         


scheduler.add_job(func=Scheduler.wake_me_up_job, trigger="interval",  minutes=20)
scheduler.start()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.debug("Request body1: " + body)
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    # if event is MessageEvent and message is TextMessage, then echo text

    try:
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue

            if isinstance(event, MessageEvent):
                messageText = event.message.text
                returnText = ""
                if (messageText == "menu"):      
                    line_bot_api.reply_message(event.reply_token, featureMenu.menu)
                elif (messageText == "設定提醒"):
                    id = ""
                    if (event.source.type == "group"):
                        id =  event.source.group_id
                    else:
                        id =  event.source.user_id
                    returnText = notifyMenu.insertId(id) 
                elif (messageText == "取消提醒"):    
                    id = ""
                    if (event.source.type == "group"):
                        id =  event.source.group_id
                    else:
                        id =  event.source.user_id
                    returnText = notifyMenu.deleteId(id) 
                elif (messageText == "誰去買樂透"):
                    line_bot_api.reply_message(event.reply_token,  FlexSendMessage(
                        alt_text = "誰去買樂透",
                        contents = shiftMenu.shift()
                    ))
                elif (messageText.startswith("儲存號碼")):
                    returnText = saveMenu.save(messageText[len("儲存號碼"):])
                elif (messageText.startswith("對獎")):
                    line_bot_api.reply_message(event.reply_token,  FlexSendMessage(
                        alt_text = "快來看看中獎了沒",
                        contents = rewMenu.targetReward(messageText[len("對獎"):])
                    ))  
                if (returnText != ""):
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=returnText))  
                             
    except RuntimeError as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(e)))                   

    return 'OK'
@app.route("/", methods=['GET'])
def wake_up():
    return 'OK'


if __name__ == "__main__":
    
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
