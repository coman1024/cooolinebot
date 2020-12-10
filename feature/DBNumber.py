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

  def getKeyinNm(date):
    with CursorFromConnectionFromPool() as mydbconn:
      sql =  "SELECT date, num FROM lottery.\"NumTbl\" WHERE type = 1 AND \"bcDate\"  <= now() AND date LIKE %s  ORDER BY date DESC LIMIT 12"
      mydbconn.execute(sql,(f'{date}%', ))
      record = mydbconn.fetchall()

    return record  

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


 
  