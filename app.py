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
    MessageTemplateAction,
    PostbackTemplateAction
)

from menu import (
    featureMenu,
    queryMenu, 
    rewMenu,
    saveMenu
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
            if messageText.startswith("#"):
                messageText = messageText[1:]
                if  (messageText == "樂透"):      
                    line_bot_api.reply_message(  
                        event.reply_token, featureMenu.menu   
                    )
                else:
                    line_bot_api.reply_message(  
                    event.reply_token, TextSendMessage(text=defaultText)   
                )
                
        elif isinstance(event, PostbackEvent):  # 如果有回傳值事件 
            returnText = defaultText
            data = event.postback.data.split('&')
            
            if data[0] == "query":
                eventCommand = data[1]
                menuCommend = queryMenu.menuCommend()
                if (eventCommand == "0"): 
                    line_bot_api.reply_message(  
                        event.reply_token, queryMenu.menu   
                    )
                elif (eventCommand == "1"):      
                    returnText = menuCommend.command1().messageText
                elif (eventCommand == "2"):
                    returnText = menuCommend.command2().messageText
                elif (eventCommand == "3"):
                    returnText = menuCommend.command3().messageText

            elif data[0] == "rew":
                eventCommand = data[1]
                menuCommend = rewMenu.menuCommend()
                if (eventCommand == "0"): 
                    line_bot_api.reply_message(  
                        event.reply_token, rewMenu.menu   
                    )
                elif (eventCommand == "1"):      
                    returnText = menuCommend.command1().messageText
                elif (eventCommand == "2"):
                    returnText = menuCommend.command2().messageText
                elif (eventCommand == "3"):
                    returnText = menuCommend.command3().messageText

            elif data[0] == "save":
                eventCommand = data[1]
                menuCommend = saveMenu.menuCommend()
                if (eventCommand == "0"): 
                    line_bot_api.reply_message(  
                        event.reply_token, saveMenu.menu   
                    )
                elif (eventCommand == "1"):      
                    returnText = menuCommend.command1().messageText
                elif (eventCommand == "2"):
                    returnText = menuCommend.command2().messageText
                elif (eventCommand == "3"):
                    returnText = menuCommend.command3().messageText 
                elif (eventCommand == "4"):
                    returnText = menuCommend.command4().messageText 

            line_bot_api.reply_message(  
                event.reply_token, TextSendMessage(text=returnText)   
            )        
            
    return 'OK'

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
