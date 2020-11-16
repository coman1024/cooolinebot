import requests
import re
from bs4 import BeautifulSoup

response = requests.get("https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx")

soup = BeautifulSoup(response.text, "html.parser")
lottoHistoryTable = soup.find("table", id="Lotto649Control_history_dlQuery")
class Crawler():
  def __init__(self):
    print("crawler!")

  def findByDate(self, varDate):
    date = lottoHistoryTable.find_all(
      "span", 
      id = re.compile("Lotto649Control_history_dlQuery_L649_DDate")
    )
    targetIdx = 99
    for idx, item  in enumerate(date):
      if varDate == item.text:
        targetIdx = idx
        break
    
    #TODO if targetIdx = 99 thorws error
    if (targetIdx == 99):
      return "找不到開獎日期"
    goldNumber = self.getNumber(targetIdx)
    return goldNumber

  def findNewNumber(self):
    return self.getNumber(0)

  def findNewDate(self):
    date = lottoHistoryTable.find("span", id = re.compile("Lotto649Control_history_dlQuery_L649_DDate_0"))
    return date.text

  def getNumber(self, targetIdx): 
    num1 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No1_" + str(targetIdx)))
    num2 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No2_" + str(targetIdx)))
    num3 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No3_" + str(targetIdx)))
    num4 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No4_" + str(targetIdx)))
    num5 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No5_" + str(targetIdx)))
    num6 = lottoHistoryTable.find("span", id = ("Lotto649Control_history_dlQuery_No6_" + str(targetIdx)))

    goldNumber = num1.text + "," + num2.text + ","  + num3.text + ","  + num4.text + ","  + num5.text + ","  + num6.text
    return goldNumber
  
