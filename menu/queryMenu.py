
from linebot import (
    LineBotApi
)
from linebot.models import (
   MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction
)

class menuCommend():  
    class command1():
        label = "查詢最新中獎號碼"
        text = "#查詢最新中獎號碼"
        data = "query&1"
    
    class command2():
        label = "日期查詢"
        text =  "#日期查詢"
        data = "query&2"
    
    class command3():
        label = "期數查詢"
        text = "#期數查詢"
        data = "query&3"

menu = TemplateSendMessage(
    alt_text = '查詢號碼功能選單',
    template = ButtonsTemplate(
        title = '你想要查詢什麼勒',
        text = '請選擇功能',
        actions = [
            PostbackTemplateAction(
                label = menuCommend.command1().label,
                text = menuCommend.command1().text,
                data = menuCommend.command1().data
            ),
            PostbackTemplateAction(
                label = menuCommend.command2().label,
                text = menuCommend.command2().text,
                data = menuCommend.command2().data
            ),
            PostbackTemplateAction(
                label = menuCommend.command3().label,
                text = menuCommend.command3().text,
                data = menuCommend.command3().data
            )
        ]
    )
)
