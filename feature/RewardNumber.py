
class rewardBot:
  glodNumber = []
  glodNumberS = "0"
  slefNumber = ["6", "12", "24", "25", "33", "35"]
  def __init__(self):
    print("rewardBot!")

  def setGlodNumber(self, glodNumber):
    self.glodNumber = glodNumber[0:5]
    self.glodNumberS = glodNumber[6]
   
  def rewardNm(self, targetNumber):
    glodNumberCount = len(set(self.glodNumber) & set(targetNumber))
    isGlodNumberS  = self.glodNumberS in targetNumber

    result = "槓龜拉"
    if glodNumberCount == 6:
      result = "全中, 恭喜頭獎"
    elif glodNumberCount == 5:
      if isGlodNumberS:
        result = "中5個+特別號, 二獎！"
      else:
        result = "中5個, 三獎！"
    elif glodNumberCount == 4:
      if isGlodNumberS:
        result = "中4個+特別號, 四獎！"
      else:
        result = "中4個, 五獎 2000元！"
    elif glodNumberCount == 3:
      if isGlodNumberS:
        result = "中3個+特別號, 六獎 1000元！"
      else:
        result = "中3個, 普獎 400元！"
    elif glodNumberCount == 2 and isGlodNumberS:
      result = "中3個, 七獎 400元！"

    gmsResult = "沒中"
    if  (isGlodNumberS):
      gmsResult = "有中"

    return "自選號碼："+ str(targetNumber) + "\n 獎號： " + str(self.glodNumber) + ", 特別號：" + self.glodNumberS + "\n 結果：中" + str(glodNumberCount) + "個, 特別號：" + gmsResult + ", " + result  

  # 自選對獎
  def rewardFixedNum(self, glodNumber):
    self.setGlodNumber(glodNumber)
    return self.rewardNm(self.slefNumber)

  # 電選對獎 TODO

  # 輸入號碼對獎
  def rewardKeyinNum(self, glodNumber, keyinNum):
    slef.setGlodNumber(glodNumber)
    return self.rewardNm(keyinNum)
    
  
 
    