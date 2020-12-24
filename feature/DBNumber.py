from config.dbConfig import CursorFromConnectionFromPool
from config.dbConfig import Database
from feature import Util
Database.initialize()

class NumberTbl:
    def getfixedNm():
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "SELECT num FROM lottery.\"NumTbl\" WHERE type = 0"
            mydbconn.execute(sql,())
            record = mydbconn.fetchone()
        return Util.toIntList(record[0].split(',', -1))

    def getKeyinNm(drawDate):
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "SELECT \"drawDate\", num FROM lottery.\"NumTbl\" WHERE type = 1 AND \"date\"  <= now() AND \"drawDate\" LIKE %s  ORDER BY \"drawDate\" DESC LIMIT 12"
            mydbconn.execute(sql,(f'{drawDate}%', ))
            record = mydbconn.fetchall()
        return record  


    def findNm(type, drawDate):
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "SELECT num FROM lottery.\"NumTbl\" WHERE type = %s AND \"drawDate\" = %s"
            mydbconn.execute(sql,(type, drawDate, ))
            record = mydbconn.fetchone()
        return record  

    def insertNm(type, drawDate, number, date):
        with CursorFromConnectionFromPool() as mydbconn:
            sql = "INSERT INTO lottery.\"NumTbl\"(type, \"drawDate\", num, date) VALUES (%s, %s, %s, %s)"
            mydbconn.execute(sql,(type, drawDate, number, date, ))
        return 

    def updateNm(type, drawDate, number):
        with CursorFromConnectionFromPool() as mydbconn:
            sql = "UPDATE lottery.\"NumTbl\" SET \"num\"=%s WHERE type=%s AND \"drawDate\"=%s "
            mydbconn.execute(sql,(number, type, drawDate, ))

class IdTbl:
    def getId(groupId):
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "SELECT \"notifyId\" FROM lottery.\"IdTbl\" WHERE \"notifyId\" = %s"
            mydbconn.execute(sql,(groupId, ))
            result = mydbconn.fetchall()
        return result

    def getIdAll():
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "SELECT * FROM lottery.\"IdTbl\""
            mydbconn.execute(sql)
            result = mydbconn.fetchall()
        return result  
        
    def insertId(id):
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "INSERT INTO lottery.\"IdTbl\" VALUES (%s)"
            mydbconn.execute(sql,(id,))

    def deleteId(id):
        with CursorFromConnectionFromPool() as mydbconn:
            sql = "DELETE FROM lottery.\"IdTbl\"  WHERE \"notifyId\" = %s"
            mydbconn.execute(sql,(id,))

class ShiftTbl:
    def getLuckyMan(shfitDate):
        with CursorFromConnectionFromPool() as mydbconn:
            sql = "SELECT \"shiftDate\", \"luckyMan\" FROM lottery.\"ShiftTbl\" WHERE \"shiftDate\" = %s "
            mydbconn.execute(sql,(shfitDate,))
            result = mydbconn.fetchone()
        return result  

    def insertLuckyMan(shfitDate ,luckyMan):
        print(f"insertLuckyMan:{luckyMan}")
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "INSERT INTO lottery.\"ShiftTbl\" VALUES (%s, %s)"
            mydbconn.execute(sql,(shfitDate,luckyMan,))
 
  