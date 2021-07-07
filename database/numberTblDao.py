from config.dbConfig import CursorFromConnectionFromPool
from feature import Util


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
