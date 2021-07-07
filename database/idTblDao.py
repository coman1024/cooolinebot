from config.dbConfig import CursorFromConnectionFromPool

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
