from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction
)

from feature import LotteryNumber

class menuCommend():  
    class command1():
        lotteryBot = LotteryNumber.LotteryNumber()
        label = "查詢最新中獎號碼"
        text = "查詢最新中獎號碼"
        data = "query&1"
        messageText = "最新一期得獎號碼：\n" + lotteryBot.findNewDate() + '\n' + lotteryBot.findByDate(lotteryBot.findNewDate())
    
    class command2():
        label = "日期查詢"
        text =  "日期查詢"
        data = "query&2"
        messageText = "請輸入 #queryD 日期(YYY/MM/DD)"
    
    class command3():
        label = "期數查詢"
        text = "期數查詢"
        data = "query&3"
        messageText = "請輸入 #queryT 期數"

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
