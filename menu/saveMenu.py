from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from feature.DBNumber import NumberTbl

class save1():
    label = "儲存自選號碼"
    text = "save1"
    def save(targetNum):
        if (len(targetNum) == 0):
            return "請輸入 save1 號碼(ex:01,02,03)"
        else: 
            return "還沒寫啦"

class save2():
    label = "自選號碼查詢"
    text =  "save2"
    def save():
        return NumberTbl.getfixedNm()

class save3():
    label = "儲存電選號碼"
    text = "save3"
    def save(targetNum):
        if (len(targetNum) == 0):
            return "請輸入 save3 號碼 日期(ex:01,02,03... 109/11/11)"
        else: 
            return "還沒寫啦"

class save4():
    label = "陰陽人爛屁股"
    text = "你罵我陰陽人爛屁股"
    def save():
        return "誰答腔我就罵誰"

menu = TemplateSendMessage(
    alt_text = '查詢號碼功能選單',
    template = ButtonsTemplate(
        title = '你想要查詢什麼勒',
        text = '請選擇功能',
        actions = [
            MessageTemplateAction(
                label = save1.label,
                text = save1.text
            ),
            MessageTemplateAction(
                label = save2.label,
                text = save2.text
            ),
            MessageTemplateAction(
                label = save3.label,
                text = save3.text
            ),
            MessageTemplateAction(
                label = save4.label,
                text = save4.text
            )
        ]
    )
)
