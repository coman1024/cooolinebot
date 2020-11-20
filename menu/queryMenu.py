from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from feature.LotteryNumber import lotteryBot
lottery_bot = lotteryBot()
class query1:
    label = "查詢最新中獎號碼"
    text = "query1"
    def find():
        date =  lottery_bot.findNewDate()
        lottery_bot.findByDate(date)
        return "最新一期得獎號碼：\n" + date + '\n' + lottery_bot.numberToStr()
        
class query2:
    label = "日期查詢"
    text = "query2"
    def find(date):
        if (len(date)== 0):
            return "請輸入 query2 日期(YYY/MM/DD)"
        try:
            lottery_bot.findByDate(date)
            return lottery_bot.numberToStr()
        except Exception as e:
            return str(e)

class query3:
    label = "期數查詢"
    text = "query3"
    def find(term):
        if(len(term) == 0):
            return "請輸入 query3 期數"
        try:
            lottery_bot.findByTerm(term)     
            return lottery_bot.numberToStr()
        except Exception as e:
            return str(e)

menu = TemplateSendMessage(
    alt_text = '查詢號碼功能選單',
    template = ButtonsTemplate(
        title = '你想要查詢什麼勒',
        text = '請選擇功能',
        actions = [
            MessageTemplateAction(
                label = query1.label,
                text = query1.text
            ),
            MessageTemplateAction(
                label = query2.label,
                text = query2.text
            ),
            MessageTemplateAction(
                label = query3.label,
                text = query3.text
            )
        ]
    )
)
