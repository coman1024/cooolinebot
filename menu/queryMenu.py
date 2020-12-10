from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from feature import lottery
from feature.lottery import Lottery649
    
from feature import Util
class query1:
    label = "查詢最新中獎號碼"
    text = "query1"
    def find():
        lottery649_lastest = lottery.scrape_lottery649_lastest()
        return template.queryResultTemplate(query1.label, "日期", lottery649_lastest.drawing_date, lottery649_lastest.winning_numbers, lottery649_lastest.special_number)
        
class query2:
    label = "日期查詢"
    text = "query2"
    def find(date):
        if (len(date)== 0):
            raise  RuntimeError("請輸入 query2 日期(YYY/MM/DD)")
        try:
            lottery649 = lottery.scrape_lottery649_by_date(date)
            return template.queryResultTemplate(query2.label, "日期", lottery649.drawing_date, lottery649.winning_numbers, lottery649.special_number)
        except Exception as e:
            raise e

class query3:
    label = "期數查詢"
    text = "query3"
    def find(seq):
        if(len(seq) == 0):
            raise  RuntimeError("請輸入 query3 期數")
        try:
            lottery649 = lottery.scrape_lottery649_by_seq(seq)    
            return template.queryResultTemplate(query3.label, "期數", seq, lottery649.winning_numbers, lottery649.special_number)
        except Exception as e:
            raise e

class template: 
    def queryResultTemplate(title, searchType, searchValue, winning_numbers, special_number):
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": f"{title}",
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
                        "text": f'{searchType}：',
                        "size": "sm",
                        "color": "#aaaaaa",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": f"{searchValue}",
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
                        "text": f"{Util.formatNumberList(winning_numbers)}",
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
                        "text": f"{special_number}",
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
