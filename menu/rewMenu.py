
from feature import lottery
from feature.lottery import (
    LotteryItem,
    Lottery649,
    LotteryTicket,
    Scrape
)

from feature.DBNumber import NumberTbl
from feature import Util

from typing import Dict, List, Tuple
def newestReward():
    
    pickNumbers_List = NumberTbl.findNm(None, None, Util.getToday())

    if len(pickNumbers_List) == 0:
        raise RuntimeError(f"自動對獎：你沒有買{targetDate}的樂透")
    return reward(pickNumbers_List)

def targetReward(targetDate):
    targetDate = Util.getCommond(targetDate)
    if len(targetDate) == 0:
        targetDate = None
    pickNumbers_List = NumberTbl.findNm(None, targetDate, None)

    if len(pickNumbers_List) == 0:
        raise RuntimeError(f"你沒有買{targetDate}的樂透")

    return reward(pickNumbers_List)
    
def reward(pickNumbers_List: list):
    resultList = []
    scrape = Scrape()
    for obj in pickNumbers_List:
        drawing_date = obj[0]
        pick_numbers = Util.toIntList(obj[1].split(',', -1))
        type = obj[2]
        ticket = LotteryTicket(LotteryItem.Lottery649, "", drawing_date, 50, pick_numbers)
        try:
            lottery649 = lottery.scrape_lottery649_by_date(scrape, drawing_date)
            lotteryPrize = lottery.lottery649_checker(lottery649, ticket)
            result = "槓龜"
            if (lotteryPrize != None):
                result = f"{lotteryPrize.title} {lotteryPrize.description}"
            resultObj = TemplateObj(type, ticket.pick_numbers, drawing_date, lottery649.winning_numbers, lottery649.special_number, result)
        except Exception as e:
            result = str(e)
            resultObj = TemplateObj(type, ticket.pick_numbers, drawing_date, " ", " ", result)

        resultList.append(resultObj)
    return template.queryResultListTemplate(resultList) 





class TemplateObj:
    def __init__(self, title: str, pick_numbers: List[int], drawing_date: str, winning_numbers: List[int], special_number:int, result:str):
        self.title = title
        self.pick_numbers = pick_numbers
        self.drawing_date = drawing_date
        self.winning_numbers = winning_numbers
        self.special_number = special_number
        self.result = result

class template: 
    
    def queryResultListTemplate(resultList):
        bubleTemplateContents = template.getResultBubbleTemplate( resultList)
        contents = {
            "type": "carousel",
            "contents" : []
        }
        bubbleTemplate = bubleTemplateContents["contents"]
        contents["contents"] = bubbleTemplate
        print(contents)
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
                            "text": "自選號碼" if item.title == 0 else "電選號碼",
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
