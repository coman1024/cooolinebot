from database.idTblDao import IdTbl


def insertId(id):
    if not id:
        raise RuntimeError("設定失敗, 找不到id資訊") 
    isHas = IdTbl.getId(id)
    if isHas:
      raise RuntimeError("已設定過") 
    try:
        IdTbl.insertId(id)
        return "設定成功"
    except RuntimeError:
        return "設定失敗"  

def getIdAll():
  idList = IdTbl.getIdAll()
  return idList

def deleteId(id):
    if not id:
        raise RuntimeError("取消失敗, 找不到id資訊") 
    isHas = IdTbl.getId(id)
    if not isHas:
      raise RuntimeError("你根本沒有設定提醒") 
    try:
        IdTbl.deleteId(id)
        return "取消成功"
    except RuntimeError:
        return "取消失敗" 


