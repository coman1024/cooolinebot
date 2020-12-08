
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from feature.LotteryNumber import lotteryBot
from feature import lottery
from feature.lottery import (
    LotteryItem,
    Lottery649,
    LotteryTicket
)

from feature.RewardNumber import rewardBot
from feature import DBNumber
from feature import Util

from typing import Dict, List, Tuple

class reward1:
    label = "自選號碼最新對獎結果"
    text = "reward1"
    def reward():
        lottery649 = lottery.scrape_lottery649_lastest()
        fixedNumbers = DBNumber.getfixedNm()
        
        ticket = LotteryTicket(LotteryItem.Lottery649, "", lottery649.drawing_date, 50, fixedNumbers)
        lotteryPrize = lottery.lottery649_checker(lottery649, ticket)
        result = "槓龜"
        if (lotteryPrize != None):
            result = f"{lotteryPrize.title} {lotteryPrize.description}"
        resultObj = TemplateObj(reward1.label, fixedNumbers, lottery649.drawing_date, lottery649.winning_numbers, lottery649.special_number, result)  
        return template.queryResultTemplate(resultObj)

class reward2:
    label = "電選號碼對獎"
    text =  "reward2"
    def reward(targetDate):
        if(len(targetDate) == 0):
            raise RuntimeError("請輸入 reward2 日期")
        resultList = []
        keyinNumberList = DBNumber.getKeyinNm(targetDate)
        if(len(keyinNumberList) == 0):
            raise RuntimeError("無此日期")

        for obj in keyinNumberList:
            drawing_date = obj[0]
            pick_numbers = obj[1].split(',', -1)
            ticket = LotteryTicket(LotteryItem.Lottery649, "", drawing_date, 50, pick_numbers)
            try:
                lottery649 = lottery.scrape_lottery649_by_date(drawing_date)
                lotteryPrize = lottery.lottery649_checker(lottery649, ticket)
                result = "槓龜"
                if (lotteryPrize != None):
                    result = f"{lotteryPrize.title} {lotteryPrize.description}"
                resultObj = TemplateObj(reward2.label, ticket.pick_numbers, drawing_date, lottery649.winning_numbers, lottery649.special_number, result)
            except Exception as e:
                result = str(e)
                resultObj = TemplateObj(reward2.label, ticket.pick_numbers, drawing_date, " ", " ", result)

            resultList.append(resultObj)
         

        return template.queryResultListTemplate(resultList)  

class reward3:
    label = "輸入號碼對獎"
    text = "reward3"
    def reward(targetNum):
        if(len(targetNum) == 0):
            raise RuntimeError("請輸入 reward3 號碼,隔開(01,02,03,04,05,06)")
        try:
            lottery649 = lottery.scrape_lottery649_lastest()
            pick_numbers = Util.toIntList(targetNum.split(',', -1))
            ticket = LotteryTicket(LotteryItem.Lottery649, "", lottery649.drawing_date, 50, pick_numbers)
            lotteryPrize = lottery.lottery649_checker(lottery649, ticket)
            result = "槓龜"
            if (lotteryPrize != None):
                result = f"{lotteryPrize.title} {lotteryPrize.description}"
            resultObj = TemplateObj(reward3.label, ticket.pick_numbers, lottery649.drawing_date, lottery649.winning_numbers, lottery649.special_number, result)  
            return template.queryResultTemplate(resultObj)

        except Exception as e:
            print(str(e))
            raise e    

class TemplateObj:
    def __init__(self, title: str, pick_numbers: List[int], drawing_date: str, winning_numbers: List[int], special_number:int, result:str):
        self.title = title
        self.pick_numbers = pick_numbers
        self.drawing_date = drawing_date
        self.winning_numbers = winning_numbers
        self.special_number = special_number
        self.result = result

class template: 
    def queryResultTemplate(tempObj:TemplateObj):
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": tempObj.title,
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": Util.formatNumberList(tempObj.pick_numbers),
                    "weight": "bold",
                    "size": "lg",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "日期：",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": tempObj.drawing_date,
                            "size": "sm",
                            "color": "#111111",
                            "align": "start"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "中獎號碼：",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": Util.formatNumberList(tempObj.winning_numbers),
                            "size": "sm",
                            "color": "#111111",
                            "align": "start"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "特別號：",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"{tempObj.special_number}",
                            "size": "sm",
                            "color": "#111111",
                            "align": "start"
                        }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": tempObj.result,
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        }
                        ]
                    }
                    ]
                }
                ]
            }
        }   
                
        return contents

    def queryResultListTemplate(resultList):
        bubleTemplateContents = template.getResultBubbleTemplate( resultList)
        contents = {
            "type": "carousel",
            "contents" : []
        }
        bubbleTemplate = bubleTemplateContents["contents"]
        contents["contents"] = bubbleTemplate
        return contents
    def getResultBubbleTemplate(resultList):
        contents = {"contents":[]}
        for item in resultList:
            contents["contents"].append( 
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "電腦選號自動對獎",
                            "weight": "bold",
                            "color": "#1DB446",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": str(item.drawing_date),
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md"
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0,
                                    "text": "你的號碼："
                                },
                                {
                                    "type": "text",
                                    "text": Util.formatNumberList(item.pick_numbers),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "中獎號碼：",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": Util.formatNumberList(item.winning_numbers),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "特別號：",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(item.special_number),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "結果：",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": item.result,
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            }
                            ]
                        }
                        ]
                    }
                }
            )
        return contents       




menu = TemplateSendMessage(
    alt_text = '對獎功能選單',
    template = ButtonsTemplate(
        title = '你想要中什麼獎勒',
        text = '請選擇功能',
        actions = [
            MessageTemplateAction(
                label = reward1.label,
                text = reward1.text
            ),
            MessageTemplateAction(
                label = reward2.label,
                text = reward2.text
            ),
            MessageTemplateAction(
                label = reward3.label,
                text = reward3.text
            )
        ]
    )
)
