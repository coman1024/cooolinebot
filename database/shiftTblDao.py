from config.dbConfig import CursorFromConnectionFromPool
from feature import Util

class ShiftTbl:
    def getLuckyMan(shfitDate):
        with CursorFromConnectionFromPool() as mydbconn:
            sql = "SELECT \"shiftDate\", \"luckyMan\" FROM lottery.\"ShiftTbl\" WHERE \"shiftDate\" = %s "
            mydbconn.execute(sql,(shfitDate,))
            result = mydbconn.fetchone()
        return result  

    def checkBeforeTimes():
        with CursorFromConnectionFromPool() as mydbconn:
            sql = "select \"luckyMan\" from lottery.\"ShiftTbl\" order by \"shiftDate\" DESC LIMIT 2"   
            mydbconn.execute(sql)
            result = mydbconn.fetchall() 
        return result

    def insertLuckyMan(shfitDate ,luckyMan):
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "INSERT INTO lottery.\"ShiftTbl\" VALUES (%s, %s)"
            mydbconn.execute(sql,(shfitDate,luckyMan,)) 