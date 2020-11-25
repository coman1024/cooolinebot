from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from feature.LotteryNumber import lotteryBot
from feature import Util
class query1:
    label = "查詢最新中獎號碼"
    text = "query1"
    def find():
        lottery_bot = lotteryBot()
        drawDate =  lottery_bot.findNewestDate()
        lottery_bot.findByDate(drawDate)
        return template.queryResultTemplate(query1.label, drawDate, lottery_bot.goldNumber, lottery_bot.goldNumberS)
        
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

class template: 
    def queryResultTemplate(title, drawDate, goldNumber, goldNumberS):
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "開獎日期：",
                        "size": "sm",
                        "color": "#aaaaaa",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": drawDate,
                        "color": "#000000",
                        "size": "sm",
                        "align": "start"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "中獎號碼：",
                        "size": "sm",
                        "color": "#aaaaaa",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": Util.formatNumberList(goldNumber),
                        "color": "#000000",
                        "size": "sm",
                        "align": "start"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "特別號：",
                        "size": "sm",
                        "color": "#aaaaaa",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": goldNumberS,
                        "color": "#000000",
                        "size": "sm",
                        "align": "start"
                    }
                    ]
                }
                ]
            }
        }
        return contents

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
