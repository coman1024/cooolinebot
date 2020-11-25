
class rewardBot:
  fixedNumber = ["6", "12", "24", "25", "33", "35"]
   
  def rewardNm(goldNumber, goldNumberS, targetNumber):

    for idx, item  in enumerate(targetNumber):
      if len(item) == 1:
        targetNumber[idx] = f'0{item}'

    goldNumberCount = len(set(goldNumber) & set(targetNumber))
    isgoldNumberS  = goldNumberS in targetNumber

    result = "槓龜拉"
    if goldNumberCount == 6:
      result = "全中, 恭喜頭獎"
    elif goldNumberCount == 5:
      if isgoldNumberS:
        result = "二獎！"
      else:
        result = "三獎！"
    elif goldNumberCount == 4:
      if isgoldNumberS:
        result = "四獎！"
      else:
        result = "五獎 2000元！"
    elif goldNumberCount == 3:
      if isgoldNumberS:
        result = "六獎 1000元！"
      else:
        result = "普獎 400元！"
    elif goldNumberCount == 2 and isgoldNumberS:
      result = "七獎 400元！"

    gmsResult = "Ｘ"
    if  (isgoldNumberS):
      gmsResult = "Ｏ"

    return f'中{str(goldNumberCount)}個, 特別號：{gmsResult},  {result}' 

    
  
 
    