import requests
import re
from bs4 import BeautifulSoup

response = requests.get("https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx")

soup = BeautifulSoup(response.text, "html.parser")
lottoHistoryTable = soup.find("table", id="Lotto649Control_history_dlQuery")
class LotteryNumber():
  def __init__(self):
    print("LotteryNumber!")
  
  #查詢最新
  def findNewNumber(self):
    return self.getNumber(0)

  #查詢by日期
  def findByDate(self, targetDate):
    date = lottoHistoryTable.find_all(
      "span", 
      id = re.compile("Lotto649Control_history_dlQuery_L649_DDate")
    )
    targetIdx = 99
    for idx, item  in enumerate(date):
      if targetDate == item.text:
        targetIdx = idx
        break
    
    #TODO if targetIdx = 99 thorws error
    if (targetIdx == 99):
      return "找不到開獎日期"
    goldNumber = self.getNumber(targetIdx)
    return goldNumber

  #查詢by期數
  def findByTerm(self, targetTern):
    tern = lottoHistoryTable.find_all(
      "span", 
      id = re.compile("Lotto649Control_history_dlQuery_L649_DrawTerm")
    )
    targetIdx = 99
    for idx, item  in enumerate(tern):
      if targetTern == item.text:
        targetIdx = idx
        break
    
    #TODO if targetIdx = 99 thorws error
    if (targetIdx == 99):
      return "找不到開獎期數"
    goldNumber = self.getNumber(targetIdx)
    return goldNumber

  def findNewDate(self):
    date = lottoHistoryTable.find("span", id = re.compile("Lotto649Control_history_dlQuery_L649_DDate_0"))
    return date.text

  def findNewTern(self):
    tern = lottoHistoryTable.find("span", id = re.compile("Lotto649Control_history_dlQuery_L649_DrawTerm_0"))
    return tern.text

  def getNumber(self, targetIdx): 
    num1 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No1_" + str(targetIdx)))
    num2 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No2_" + str(targetIdx)))
    num3 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No3_" + str(targetIdx)))
    num4 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No4_" + str(targetIdx)))
    num5 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No5_" + str(targetIdx)))
    num6 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No6_" + str(targetIdx)))

    goldNumber = num1.text + "," + num2.text + ","  + num3.text + ","  + num4.text + ","  + num5.text + ","  + num6.text
    return goldNumber
  
