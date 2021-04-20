from feature.DBNumber import ShiftTbl
from feature.shiftScheduler import (
    ShiftScheduler,
    ShiftInfo
)
from feature import Util

def shift():
    shiftDate = Util.getShiftDate()
    luckyMan = getLuckyMan(shiftDate)
    nextShiftDate = Util.getNextShiftDate()
    nextLuckyMan = getLuckyMan(nextShiftDate)

    shiftInfo = ShiftInfo(shiftDate, luckyMan)
    nextShiftInfo = ShiftInfo(nextShiftDate, nextLuckyMan)
    return template.shiftResultTemplate(shiftInfo, nextShiftInfo)


def getLuckyMan(shiftDate):
    luckyMan = ""
    shiftTbl = ShiftTbl.getLuckyMan(shiftDate)
    # breakpoint()
    if shiftTbl:
        luckyMan = shiftTbl[1]
    else:
        checkTimes = ShiftTbl.checkBeforeTimes()
        isRepeat = False
        if (checkTimes and (checkTimes[0][0] == checkTimes[1][0])):
            while True:
                luckyMan = ShiftScheduler.randomShift()
                isRepeat = (checkTimes[1][0] == luckyMan)
                if not isRepeat:
                    break 
        else:                
            luckyMan = ShiftScheduler.randomShift()

        # ShiftTbl.insertLuckyMan(shiftDate, luckyMan)
    return luckyMan  

class template: 
    def shiftResultTemplate(shiftInfo: ShiftInfo, nextShiftInfo: ShiftInfo):
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "誰去買樂透",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
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
                            "text": f"當月({shiftInfo.shiftDate})",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": shiftInfo.luckyMan,
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
                            "text": f"下個月({nextShiftInfo.shiftDate})",
                            "size": "sm",
                            "color": "#555555"
                        },
                        {
                            "type": "text",
                            "text": nextShiftInfo.luckyMan,
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
        return contents        



    

