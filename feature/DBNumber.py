from config.dbConfig import CursorFromConnectionFromPool
from config.dbConfig import Database
from feature import Util
import datetime 
Database.initialize()

class NumberTbl:
    def getfixedNm():
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "SELECT num FROM lottery.\"NumTbl\" WHERE type = 0"
            mydbconn.execute(sql,())
            record = mydbconn.fetchone()
        return Util.toIntList(record[0].split(',', -1))

    def findNm(type, drawDate, date):
        with CursorFromConnectionFromPool() as mydbconn:
            condistions = []
            sql =  "SELECT \"drawDate\", num, \"type\" FROM lottery.\"NumTbl\" WHERE 1=1 "
            condistionSQL = ""
            if type:
                condistionSQL += " and \"type\"=%s "
                condistions.append(type)
            if drawDate:
                condistionSQL += " and \"drawDate\"=%s "
                condistions.append(drawDate)
            if date:
                condistionSQL += " and \"date\"=%s "
                condistions.append(date)

            if len(condistionSQL) == 0:
                condistionSQL += " and \"date\" <= now() "
            sql += condistionSQL  
            sql += " ORDER BY \"date\" DESC, \"type\" LIMIT 12"
            mydbconn.execute(sql,(condistions))
            record = mydbconn.fetchall()
        return record

    def insertNm(type, drawDate, number, date):
        with CursorFromConnectionFromPool() as mydbconn:
            sql = "INSERT INTO lottery.\"NumTbl\"(type, \"drawDate\", num, date) VALUES (%s, %s, %s, %s)"
            mydbconn.execute(sql,(type, drawDate, number, date, ))

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

class Ledger:
    
    def __init__(self, owner: str, amount: int, payDate: str, createUser: str, *createDate: str):
        self.owner = owner
        self.amount = amount
        self.payDate = payDate 
        self.createUser = createUser
        self.createDate = createDate
        
    
    def saveToDb(self):
        LedgerMoney.insertMoney(self.owner, self.amount, self.payDate, self.createUser)

    def updateToDb(self):
        LedgerMoney.updateAmount(self.owner, self.amount, self.payDate)

class LedgerMoney:
   
    def getMoneyByPayDate(*payDate):

        with CursorFromConnectionFromPool() as mydbconn:
            sql = "SELECT * FROM lottery.\"LedgerTbl\" "

            if payDate and len(payDate)!=1:
                sql += "WHERE \"payDate\" = %s "
            sql += "ORDER BY \"payDate\" LIMIT 4 "

            mydbconn.execute(sql,(*payDate,))
            result = mydbconn.fetchall()

            resultList = []
            for x in result:
                resultList.append(Ledger(x[0], x[1], x[2], x[3]))
        return resultList  
    
    def insertMoney(owner, amount, paydate, createUser):
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "INSERT INTO lottery.\"LedgerTbl\" VALUES (%s, %s, %s, %s, current_timestamp)"
            return mydbconn.execute(sql,(owner,amount, paydate, createUser))

    def updateAmount(owner, amount, paydate):
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "UPDATE lottery.\"LedgerTbl\" SET \"amount\" = %s WHERE \"owner\" = %s AND \"payDate\" =%s"
            return mydbconn.execute(sql,(amount, owner, paydate))
  