from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction
)

class menuCommend():  
    class command1():
        label = "查詢中獎號碼"
        text = "查詢中獎號碼"
        data = "query&0"
    
    
    class command2():
        label = "對獎"
        text =  "對獎"
        data = "rew&0"
    
    class command3():
        label = "儲存號碼"
        text = "儲存號碼"
        data = "save&0"

menu = TemplateSendMessage(
    alt_text = '樂透功能選單',
    template = ButtonsTemplate(
        title = '你想要做什麼勒',
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
