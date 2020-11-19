
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction
)

class menuCommend():  
    class command1():
        label = "自選號碼對獎"
        text = "自選對獎"
        data = "rew&1"
        messageText = "回覆最新一期API"
    
    class command2():
        label = "電選號碼對獎"
        text =  "電選對獎"
        data = "rew&2"
        messageText = "回覆最新一期API"
    
    class command3():
        label = "輸入號碼對獎"
        text = "輸入號碼對獎"
        data = "rew&3"
        messageText = "請輸入 #rew 號碼,隔開(01,02,03,04,05,06)"

menu = TemplateSendMessage(
    alt_text = '對獎功能選單',
    template = ButtonsTemplate(
        title = '你想要中什麼獎勒',
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
