
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from feature.LotteryNumber import lotteryBot
from feature.RewardNumber import rewardBot
from feature import DBNumber
from feature import Util


class reward1:
    label = "自選號碼最新對獎結果"
    text = "reward1"
    def reward():
        lottery_bot = lotteryBot()
        drawDate = lottery_bot.findNewestDate()
        lottery_bot.findByDate(drawDate)
        goldNumber = lottery_bot.goldNumber
        goldNumberS = lottery_bot.goldNumberS
        fixedNumber = DBNumber.getfixedNm().split(',', -1)
        
        result = rewardBot.rewardNm(goldNumber, goldNumberS, fixedNumber)
        
        return template.queryResultTemplate(reward1.label, fixedNumber, drawDate, goldNumber, goldNumberS, result)  

class reward2:
    label = "電選號碼對獎"
    text =  "reward2"
    def reward(targetDate):
        if(len(targetDate) == 0):
            raise RuntimeError("請輸入 reward2 日期")
        lottery_bot = lotteryBot()
        keyinNumberList = DBNumber.getKeyinNm(targetDate)
        resultList = {
            "resultList":[]
        }
        for obj in keyinNumberList:
            resultObj = {
                "date": "",
                "goldNumber": [],
                "goldNumberS": "",
                "keyinNum": [],
                "result": ""
            }
            goldNumber = {}
            goldNumberS = ""
            targetNum = {}
            result = ""
            try:
                lottery_bot.findByDate(obj[0])
                goldNumber = lottery_bot.goldNumber
                goldNumberS = lottery_bot.goldNumberS
                targetNum = obj[1].split(',', -1)
                result = rewardBot.rewardNm(goldNumber, goldNumberS, targetNum)
            except Exception as e:
                goldNumber = []
                goldNumberS = " "
                targetNum = obj[1].split(',', -1)
                result = str(e)
            
            resultObj["date"] = obj[0]
            resultObj["goldNumber"] = goldNumber
            resultObj["goldNumberS"] = goldNumberS
            resultObj["keyinNum"]= targetNum
            resultObj["result"]= result

            resultList["resultList"].append(resultObj)

        return template.queryResultListTemplate(targetDate, resultList)  
        
class reward3:
    label = "輸入號碼對獎"
    text = "reward3"
    def reward(targetNum):
        if(len(targetNum) == 0):
            raise RuntimeError("請輸入 reward3 號碼,隔開(01,02,03,04,05,06)")
        try:
            lottery_bot = lotteryBot()
            drawDate = lottery_bot.findNewestDate()
            lottery_bot.findByDate(drawDate)
            goldNumber = lottery_bot.goldNumber
            goldNumberS = lottery_bot.goldNumberS
            targetNumList = targetNum.split(',', -1)
            result = rewardBot.rewardNm(goldNumber, goldNumberS, targetNumList)
            return template.queryResultTemplate(reward3.label, targetNumList, drawDate, goldNumber, goldNumberS, result) 
        except Exception as e:
            print(str(e))
            raise e    

class template: 
    def queryResultTemplate(title, fixedNumber, drawDate, goldNumber, goldNumberS, result):
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
                    "type": "text",
                    "text": Util.formatNumberList(fixedNumber),
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
                            "text": drawDate,
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
                            "text": Util.formatNumberList(goldNumber),
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
                            "text": goldNumberS,
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
                            "text": result,
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

    def queryResultListTemplate(targetDate, resultList):
        bubleTemplateContents = template.getResultBubbleTemplate(targetDate, resultList)
        contents = {
            "type": "carousel",
            "contents" : []
        }
        bubbleTemplate = bubleTemplateContents["contents"]
        contents["contents"] = bubbleTemplate
        return contents
    def getResultBubbleTemplate(targetDate, resultList):
        contents = {"contents":[]}
        for item in resultList["resultList"]:
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
                            "text": targetDate,
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
                                    "text": str(item["date"])
                                },
                                {
                                    "type": "text",
                                    "text": Util.formatNumberList(item["keyinNum"]),
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
                                    "text": Util.formatNumberList(item["goldNumber"]),
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
                                    "text": item["goldNumberS"],
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
                                    "text": item["result"],
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
