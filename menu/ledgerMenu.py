from database.ledgerTblDao import LedgerTbl
from database.module.ledgerTbl import Ledger
from feature import Util
from feature.shiftScheduler import ShiftScheduler
import calendar
from calendar import weekday, monthrange 
from datetime import datetime, date
#設定繳多少錢
def getPayAmount(payDate):
    year = payDate[:4]
    month = payDate[4:]
    monthRange = calendar.monthrange(int(year), int(month))
    weekOfMonth =  [weekday(int(year), int(month), d) for d in range(1,monthRange[1])]
    termCount = weekOfMonth.count(0) + weekOfMonth.count(4)
    amount = termCount*50*2/4

    return amount
#設定下個月紀錄
def setNextLedger(payDate):
    mans = ShiftScheduler.mans
    for name in mans:
        ledger = Ledger(name, 0, payDate, "SYS")
        LedgerTbl.insertMoney(ledger)
    
# 記帳
def insertLedger(cmdStr):
    if (len(cmdStr) == 0):
        return "請輸入 記帳 人 金額(ex:[CO、YO、Feng、文B] 123)"
    else:
        cmdStr = Util.getCommond(cmdStr)
        cmd = cmdStr.split(" ",-1)
        owner = cmd[0]
        amount = cmd[1]
        if not(amount.isdigit()):
            return f"金額 {amount} 錯誤"
        ledgerList = LedgerTbl.getMoneyByPayDate()
        ledgerFilter = list(filter(lambda obj: obj.owner == owner.strip(), ledgerList))
   
        if ledgerFilter:
            ledger = ledgerFilter[0]
            ledger.amount = amount
            ledger.updateToDb()
            return f"記帳成功 ,{owner} {ledger.payDate} {amount}元"
        elif(len(ledgerFilter) == 0):    
            return f"找不到 {owner}"
        else:
            return "記帳失敗"
# 查帳
def getLedger():
    ledgerList = LedgerTbl.getMoneyByPayDate()
    contents = template.ledgerTemplate(ledgerList)

    return contents


class template:
    def getLegerStatus(amount:int):
        if (amount == 0):
            return "還不繳錢啊"
        else:
            return str(amount)+"元"

    def getLegerStatusColor(amount:int):
        if (amount == 0):
            return "#ff0000"
        else:
            return "#000000"        

    def getLedgerListTemplate(legerList: list):
        payDate = ""
        if (legerList):
            payDate = f"{legerList[0].payDate}"
        else:
            payDate = "沒有紀錄" 
        
        ledgerListSubContents = []
        for ledger in legerList:
            contentLeger = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {   
                        "type": "text",
                        "text": f"{ledger.owner}"
                    },
                    {
                        "type": "text",
                        "text": f"{template.getLegerStatus(ledger.amount)}",
                        "color": f"{template.getLegerStatusColor(ledger.amount)}"
                    }
                ]
            }

            ledgerListSubContents.append(contentLeger)

        ledgerListContents = [
            {   
                "type": "text",
                "text": payDate,
                "color": "#00CC66",
                "size": "lg"
            },
            {
                "type": "separator",
                "margin": "sm"
            } 
            ,{
                "type": "box",
                "layout": "vertical",
                "margin": "sm",
                "spacing": "sm",
                "contents": ledgerListSubContents
            }
        ]

        return ledgerListContents

    def ledgerTemplate(ledgerList: list):
        ledgerListContents = template.getLedgerListTemplate(ledgerList)
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": ledgerListContents
            }
        }

        return contents

