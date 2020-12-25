from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)


class menu1:
    label = "查詢中獎號碼"
    text = "queryM"

class menu3:
    label = "儲存號碼"
    text = "saveM"

menu = TemplateSendMessage(
    alt_text = '樂透功能選單',
    template = ButtonsTemplate(
        title = '你想要做什麼勒',
        text = '請選擇功能',
        actions = [
            MessageTemplateAction(
                label = menu1.label,
                text = menu1.text
            ),
            MessageTemplateAction(
                label = menu3.label,
                text = menu3.text
            )
        ]
    )
)
