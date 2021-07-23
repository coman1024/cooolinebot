from config.dbConfig import CursorFromConnectionFromPool
from database.module.ledgerTbl import Ledger
from feature import Util

class LedgerTbl:
   
    def getMoneyByPayDate(*payDate):

        with CursorFromConnectionFromPool() as mydbconn:
            sql = "SELECT * FROM lottery.\"LedgerTbl\" "

            if payDate and len(payDate)!=1:
                sql += "WHERE \"payDate\" = %s "
            sql += "ORDER BY \"payDate\" DESC LIMIT 4 "

            mydbconn.execute(sql,(*payDate,))
            result = mydbconn.fetchall()

            resultList = []
            for x in result:
                resultList.append(Ledger(x[0], x[1], x[2], x[3]))
        return resultList  
    
    def insertMoney(ledger):

        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "INSERT INTO lottery.\"LedgerTbl\" VALUES (%s, %s, %s, %s, current_timestamp)"
            return mydbconn.execute(sql,(ledger.owner,ledger.amount, ledger.payDate, ledger.createUser))

    def updateAmount(ledger):
        with CursorFromConnectionFromPool() as mydbconn:
            sql =  "UPDATE lottery.\"LedgerTbl\" SET \"amount\" = %s WHERE \"owner\" = %s AND \"payDate\" =%s"
            return mydbconn.execute(sql,(ledger.amount, ledger.owner, ledger.payDate))
  