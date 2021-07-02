from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)



menuList = []

menuList.append(MessageTemplateAction('查詢中獎號碼', '對獎'))
menuList.append(MessageTemplateAction('誰去買樂透', '誰去買樂透'))
menuList.append(MessageTemplateAction('儲存號碼', '儲存號碼'))
# menuList.append(MessageTemplateAction('記帳', '記帳'))
menuList.append(MessageTemplateAction('查帳', '誰還沒付錢'))
# menuList.append(MessageTemplateAction('繳錢', '要繳多少錢'))
        



menu = TemplateSendMessage(
    alt_text = '樂透功能選單',
    template = ButtonsTemplate(
        title = '你想要做什麼勒',
        text = '請選擇功能',
        actions = menuList
    )
)
