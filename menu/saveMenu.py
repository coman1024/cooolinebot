from database.numberTblDao import NumberTbl

from feature import Util



def save(cmdStr):
    if (len(cmdStr) == 0):
        return "請輸入 儲存號碼 號碼 日期(ex:01,02,03... 109/11/11)"
    else: 
        cmdStr = Util.getCommond(cmdStr)
        cmd = cmdStr.split(" ",-1)
        numbers = cmd[0]
        drawDate = cmd[1]
        date = Util.getADyear(drawDate)
        if not NumberTbl.findNm("1", drawDate, None):
            fixedNumbers = NumberTbl.getfixedNm()
            NumberTbl.insertNm("1", drawDate, numbers, date)
            NumberTbl.insertNm("0", drawDate,  Util.formatNumberList(fixedNumbers), date)
            return f"儲存成功 {cmdStr}" 
        else:    
            NumberTbl.updateNm("1", drawDate, numbers)
            return f"更新成功 {cmdStr}" 

   
                        


