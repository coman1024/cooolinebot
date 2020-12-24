from datetime import datetime, date

def formatNumberList(numbers):
    try:
        return f'{numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}, {numbers[4]}, {numbers[5]}'
    except Exception as e:
        return str(e)


def toIntList(strList):
    return [int(i) for i in strList]

def getADyear(drawDate):
    if (len(drawDate) == 9):
        date = toIntList(drawDate.split('/',-1))
        if (len(date) == 3):
            try:
                adYear = datetime(year=(date[0]+1911),month=date[1],day=date[2])
                return adYear
            except ValueError:
                raise RuntimeError("日期錯誤")
    raise RuntimeError("日期錯誤")
           
def getShiftDate():
    shiftDate = date.today()
    return shiftDate.strftime("%Y%m")

def getNextShiftDate():    
    today = date.today()
    nextShiftDate = ""
    try:
        nextShiftDate = datetime(year=today.year, month=today.month+1, day=1)
    except ValueError:
        if today.month == 12:
            nextShiftDate = datetime(year=today.year+1, month=1, day=1)
        else:
            raise RuntimeError("日期錯誤")    

    return nextShiftDate.strftime("%Y%m")

def getCommond(cmd: str):
    if(cmd.startswith(" ")):
        cmd = cmd[1:]
        return getCommond(cmd)
    else:
        return cmd    