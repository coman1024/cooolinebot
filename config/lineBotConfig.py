
import os
import sys
import re
from linebot import (
    LineBotApi, WebhookParser
)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

class LinbotConfig:

    line_bot_api = None
    parser = None
    
    # get channel_secret and channel_access_token from your environment variable
    @classmethod
    def initialize(cls, **kwargs):
        cls.line_bot_api = LineBotApi(channel_access_token)
        cls.parser = WebhookParser(channel_secret)
        print("linebot conn initialize")
    @classmethod
    def get_line_bot_api(cls):
        return cls.line_bot_api
    
    @classmethod
    def get_parser(cls):
        return cls.parser

  
    
    


