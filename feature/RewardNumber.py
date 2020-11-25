
class rewardBot:
  fixedNumber = ["6", "12", "24", "25", "33", "35"]
   
  def rewardNm(goldNumber, goldNumberS, targetNumber):
    goldNumberCount = len(set(goldNumber) & set(targetNumber))
    isgoldNumberS  = goldNumberS in targetNumber

    result = "槓龜拉"
    if goldNumberCount == 6:
      result = "全中, 恭喜頭獎"
    elif goldNumberCount == 5:
      if isgoldNumberS:
        result = "中5個+特別號, 二獎！"
      else:
        result = "中5個, 三獎！"
    elif goldNumberCount == 4:
      if isgoldNumberS:
        result = "中4個+特別號, 四獎！"
      else:
        result = "中4個, 五獎 2000元！"
    elif goldNumberCount == 3:
      if isgoldNumberS:
        result = "中3個+特別號, 六獎 1000元！"
      else:
        result = "中3個, 普獎 400元！"
    elif goldNumberCount == 2 and isgoldNumberS:
      result = "中3個, 七獎 400元！"

    gmsResult = "沒中"
    if  (isgoldNumberS):
      gmsResult = "有中"

    return "中" + str(goldNumberCount) + "個, 特別號：" + gmsResult + ", " + result  

    
  
 
    