from config.dbConfig import CursorFromConnectionFromPool
from config.dbConfig import Database
Database.initialize()


def getfixedNm():
  with CursorFromConnectionFromPool() as mydbconn:
    sql_select_query =  "select num from lottery.\"NumTbl\" WHERE type = 0"
    mydbconn.execute(sql_select_query,())
    record = mydbconn.fetchone()

  return str(record[0])

def getKeyinNm(date):
  with CursorFromConnectionFromPool() as mydbconn:
    sql_select_query =  "select date, num from lottery.\"NumTbl\" WHERE type = 1 and date like %s order by date desc limit 20"
    mydbconn.execute(sql_select_query,(f'{date}%', ))
    record = mydbconn.fetchall()

  return record  

  