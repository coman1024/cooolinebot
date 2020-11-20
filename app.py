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
    MessageTemplateAction
)

from menu import (
    featureMenu,
    queryMenu,
    rewMenu,
    saveMenu
)
from menu.featureMenu import(
    menu1,
    menu2,
    menu3
)
from menu.queryMenu import(
    query1,
    query2,
    query3
)
from menu.rewMenu import(
    reward1,
    reward2,
    reward3
)

from menu.saveMenu import(
    save1,
    save2,
    save3,
    save4
)

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
    for event in events:
        if isinstance(event, MessageEvent):
            messageText = event.message.text
            returnText = ""
            if (messageText == "menu"):      
                line_bot_api.reply_message(event.reply_token, featureMenu.menu)
            
            elif (messageText.startswith("query")):
                messageText = messageText[len("query"):]
                
                if (messageText.startswith("M")):
                    line_bot_api.reply_message(event.reply_token, queryMenu.menu)
                elif (messageText.startswith("1")):
                    returnText = query1.find()
                elif (messageText.startswith("2")):
                    returnText = query2.find(messageText[1:].strip())
                elif (messageText.startswith("3")):   
                    returnText = query3.find(messageText[1:].strip())
                
            elif (messageText.startswith("reward")):
                messageText = messageText[len("reward"):]

                if (messageText.startswith("M")):
                    line_bot_api.reply_message(event.reply_token, rewMenu.menu)
                elif (messageText.startswith("1")):
                    returnText = reward1.reward()
                elif (messageText.startswith("2")):   
                    returnText = reward2.reward()
                elif (messageText.startswith("3")):    
                    returnText = reward3.reward(messageText[1:].strip())

            elif (messageText.startswith("save")):
                messageText = messageText[len("save"):]

                if (messageText.startswith("M")):
                    line_bot_api.reply_message(event.reply_token, saveMenu.menu)
                elif (messageText.startswith("1")):
                    returnText = save1.save(messageText[1:].strip())
                elif (messageText.startswith("2")):   
                    returnText = save2.save()
                elif (messageText.startswith("3")):           
                    returnText = save3.save(messageText[1:].strip())
                
            elif (messageText == "你罵我陰陽人爛屁股"):           
                returnText = save4.save()

            if (returnText != ""):            
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=returnText))                   
       

    return 'OK'

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
