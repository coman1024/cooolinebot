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
from config import initConfig
from config.lineBotConfig import LinbotConfig
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
    shiftMenu,
    ledgerMenu
)

initConfig.initialize()

app = Flask(__name__)

print("sio start app !!")
defaultText = "查無指令"



@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    line_bot_api = LinbotConfig.get_line_bot_api()
    parser = LinbotConfig.get_parser()
    
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
                if (messageText.lower() == "help"):      
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
                elif "付錢" in messageText:
                    line_bot_api.reply_message(event.reply_token,  FlexSendMessage(
                        alt_text = "看看誰還沒付錢",
                        contents = ledgerMenu.getLedger()
                    ))
                elif (messageText.startswith("記帳")):
                    returnText = ledgerMenu.insertLedger(messageText[len("記帳"):])
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
