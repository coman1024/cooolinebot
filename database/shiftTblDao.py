from config.dbConfig import CursorFromConnectionFromPool
from feature import Util
from database.module.shiftTbl import Shift

class ShiftTbl:
    def getLuckyMan(shfitDate):
        with CursorFromConnectionFromPool() as mydbconn:
            sql = "SELECT \"shiftDate\", \"luckyMan\", \"amount\" FROM lottery.\"ShiftTbl\" WHERE \"shiftDate\" = %s "
            mydbconn.execute(sql,(shfitDate,))
            result = mydbconn.fetchone()
            if not result:
                return None
        return Shift(result[0],result[1],result[2])

    def checkBeforeTimes():
        with CursorFromConnectionFromPool() as mydbconn:
            sql = "select \"luckyMan\" from lottery.\"ShiftTbl\" order by \"shiftDate\" DESC LIMIT 2"   
            mydbconn.execute(sql)
            result = mydbconn.fetchall() 
        return result

    def insertLuckyMan(Shift):
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "INSERT INTO lottery.\"ShiftTbl\" VALUES (%s, %s, %s)"
            mydbconn.execute(sql,(Shift.shiftDate, Shift.luckyMan, Shift.amount)) 