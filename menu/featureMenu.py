
from linebot import (
    LineBotApi
)
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

class menuCommend():  
    class command1():
        label = "查詢中獎號碼"
        text = "#查詢中獎號碼"
    
    class command2():
        label = "對獎"
        text =  "#對講"
    
    class command3():
        label = "儲存號碼"
        text = "#儲存號碼"

menu = TemplateSendMessage(
    alt_text = '樂透功能選單',
    template = ButtonsTemplate(
        title = '你想要做什麼勒',
        text = '請選擇功能',
        actions = [
            MessageTemplateAction(
                label = menuCommend.command1().label,
                text = menuCommend.command1().text
            ),
            MessageTemplateAction(
                label = menuCommend.command2().label,
                text = menuCommend.command2().text
            ),
            MessageTemplateAction(
                label = menuCommend.command3().label,
                text = menuCommend.command3().text
            )
        ]
    )
)
