from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction
)

class menuCommend():  
    class command1():
        label = "儲存自選號碼"
        text = "儲存自選號碼"
        data = "save&1"
        messageText = "請輸入 #save1 號碼(ex:01,02,03)"
    
    class command2():
        label = "自選號碼查詢"
        text =  "自選號碼查詢"
        data = "save&2"
        messageText = "顯示自選號碼"
    
    class command3():
        label = "儲存電選號碼"
        text = "儲存電選號碼"
        data = "save&3"
        messageText = "請輸入 #save2 號碼 日期(ex:01,02,03... 109/11/11)"

    class command4():
        label = "驚喜按鈕"
        text = "世界上誰最智障"
        data = "save&4"
        messageText = "就是你"

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
            ),
            PostbackTemplateAction(
                label = menuCommend.command4().label,
                text = menuCommend.command4().text,
                data = menuCommend.command4().data
            )
        ]
    )
)
