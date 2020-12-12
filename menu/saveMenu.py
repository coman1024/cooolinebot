from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from feature.DBNumber import NumberTbl

from feature import Util


class save2():
    label = "查詢自選號碼"
    text =  "save2"
    def save():
        return Util.formatNumberList(NumberTbl.getfixedNm())

class save3():
    label = "儲存電選號碼"
    text = "save3"
    def save(cmdStr):
        if (len(cmdStr) == 0):
            return "請輸入 save3 號碼 日期(ex:01,02,03... 109/11/11)"
        else: 
            cmd = cmdStr.split(" ",-1)
            numbers = cmd[0]
            drawDate = cmd[1]
            date = Util.getADyear(drawDate)
            if not NumberTbl.findNm("1", drawDate):
                NumberTbl.insertNm("1", drawDate, numbers, date)
                return f"儲存成功 {cmdStr}" 
            else:    
                NumberTbl.updateNm("1", drawDate, numbers)
                return f"更新成功 {cmdStr}" 

class save4():
    label = "查詢電選號碼"
    text = "save4"
    def save(drawDat):
        if (len(drawDat) == 0):
            return "請輸入 save4 日期(YYY/MM/DD)"
        else: 
            numbers = NumberTbl.findNm("1", drawDat)
            if numbers:
                return numbers[0]
            else:
                return "找不到"    
                        

menu = TemplateSendMessage(
    alt_text = '查詢號碼功能選單',
    template = ButtonsTemplate(
        title = '你想要查詢什麼勒',
        text = '請選擇功能',
        actions = [
           
            MessageTemplateAction(
                label = save2.label,
                text = save2.text
            ),
            MessageTemplateAction(
                label = save3.label,
                text = save3.text
            ),
            MessageTemplateAction(
                label = save4.label,
                text = save4.text
            )
        ]
    )
)
