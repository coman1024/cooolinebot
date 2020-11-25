
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from feature.LotteryNumber import lotteryBot
from feature.RewardNumber import rewardBot
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
        fixedNumber = rewardBot.fixedNumber
        result = rewardBot.rewardNm(goldNumber, goldNumberS, fixedNumber)
        
        return reward1.flex_contents(fixedNumber, drawDate, goldNumber, goldNumberS, result)

    def flex_contents(fixedNumber, drawDate, goldNumber, goldNumberS, result):
       
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "自選對獎",
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

class reward2:
    label = "電選號碼對獎"
    text =  "reward2"
    def reward():
        return "還沒寫啦"
class reward3:
    label = "輸入號碼對獎"
    text = "reward3"
    def reward(targetNum):
        if(len(targetNum) == 0):
            return "請輸入 reward3 號碼,隔開(01,02,03,04,05,06)"
        try:
            return "還沒寫啦"
        except Exception as e:
            return str(e)     

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
