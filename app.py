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
    TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

import crawler.crawler


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
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        print(event.message)
        Crawler = crawler.crawler.Crawler()
    
        defaultText = "查無指令"
        returnText = defaultText
        command1 = "查詢最新"
        command2 = "這是殺小"

        if event.message.text == "安安":
            line_bot_api.reply_message(  # 回復傳入的訊息文字
                event.reply_token,
                TemplateSendMessage(
                    alt_text='樂透功能選單',
                    template=ButtonsTemplate(
                        title='你想要做什麼勒',
                        text='請選擇功能',
                        actions=[
                            MessageTemplateAction(
                                label='查詢最新一期',
                                text=command1
                            ),
                            MessageTemplateAction(
                                label='Coming Soon',
                                text=command2
                            )
                        ]
                    )
                )
            )

        else :
            returnText = defaultText

        if event.message.text == command1:
            returnText = "最新一期得獎號碼：\n" + Crawler.findNewDate() + '\n' + Crawler.findByDate(Crawler.findNewDate())
        if event.message.text == command2: 
            returnText = "還沒做好啦，點殺小"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=returnText)
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
