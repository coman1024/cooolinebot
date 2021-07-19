from database.shiftTblDao import ShiftTbl
from menu import ledgerMenu
from database.module.shiftTbl import Shift
from feature.shiftScheduler import (
    ShiftScheduler
)
from feature import Util

def shift():
    
    shiftDate = Util.getShiftDate()
    shiftInfo = getLuckyMan(shiftDate)
    nextShiftDate = Util.getNextShiftDate()
    nextShiftInfo = getLuckyMan(nextShiftDate)

    return template.shiftResultTemplate(shiftInfo, nextShiftInfo)


def getLuckyMan(shiftDate):
    
    luckyMan = ""
    shift = ShiftTbl.getLuckyMan(shiftDate)
    # breakpoint()
    if shift:
        luckyMan = shift.luckyMan
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

        payMount = ledgerMenu.getPayAmount(shiftDate)
        shift = Shift(shiftDate, luckyMan, payMount)
        ShiftTbl.insertLuckyMan(shift)
        ledgerMenu.setNextLedger(shiftDate)
    return shift

class template: 
    def shiftResultTemplate(shiftInfo: Shift, nextShiftInfo: Shift):
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
                            "text":f" {shiftInfo.luckyMan} ({shiftInfo.amount}/人)",
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
                            "text": f"{nextShiftInfo.luckyMan} ({nextShiftInfo.amount}/人)",
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



    

