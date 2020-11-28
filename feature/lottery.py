import requests
from bs4 import BeautifulSoup
import re
from enum import Enum
from typing import Dict, List, Tuple
import itertools

class LotteryPrize:
    def __init__(self, title: str, description: str, winners: int, prize_money: int, next_prize_money: int):
        self.title = title
        self.description = description
        self.winners = winners
        self.prize_money = prize_money
        self.next_prize_money = next_prize_money

class LotteryItem(Enum):
    Lottery649 = "lottery649"

class Lottery:
    def __init__(self, item: LotteryItem, period: str, drawing_date: str, due_date: str, sales_money: int, total_prize: int, prizes: Dict[Tuple[int, int], LotteryPrize]):
        self.item = item
        self.period = period
        self.drawing_date = drawing_date
        self.due_date = due_date
        self.sales_money = sales_money
        self.total_prize = total_prize
        self.prizes = prizes

class Lottery649(Lottery):
    def __init__(self, winning_numbers: List[int] , special_number: int, **kwargs):
        super().__init__(**kwargs)
        self.winning_numbers = winning_numbers
        self.special_number = special_number

class LotteryTicket:
    def __init__(self, item: LotteryItem, purchase_date: str, drawing_date: str, price: int, pick_numbers: List[int]):
        self.item = item
        self.purchase_date = purchase_date
        self.drawing_date = drawing_date
        self.price = price
        self.pick_numbers = pick_numbers

def lottery649_checker(lotto: Lottery649, ticket: LotteryTicket):
    winning_count = len(set(lotto.winning_numbers).intersection(set(ticket.pick_numbers)))
    win_special_number = lotto.special_number in ticket.pick_numbers

    winning_tuple = (winning_count, win_special_number)
    prize = lotto.prizes[winning_tuple] if winning_tuple in lotto.prizes else None
    return prize

def __generate_lottery649_prizes(winners, prize_money_list, accumalted_list):
    keys = [(6,0), (5,1), (5,0), (4,1), (4,0), (3,1), (2,1), (3,0)]
    titles = ["頭獎", "貳獎", "參獎", "肆獎", "伍獎", "陸獎", "柒獎", "普獎"]
    desc = ["6個", "任5個＋特別號", "任5個", "任4個＋特別號", "任4個", "任3個＋特別號", "任2個＋特別號", "任3個"]
    return {k : LotteryPrize(t, d, w, m, a) for (k, t, d, w, m, a) in itertools.zip_longest(keys, titles, desc, winners, prize_money_list, accumalted_list, fillvalue=None)}

def scrape_lottery649_lastest():
    response = requests.get("https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx")
    soup = BeautifulSoup(response.text, "html.parser")
    categs = [tag.string for tag in soup.find_all(id=re.compile("Lotto649Control_history_dlQuery_L649_Categ[ABC][345]_0"))]
    labels = [tag.string for tag in soup.find_all(id=re.compile("Lotto649Control_history_dlQuery_Label[0-9]+_0"))]

    winners = categs[0:3]
    winners.extend(labels[0:5])

    prize_money_list = [categs[3]]
    prize_money_list.extend(labels[5:12])

    accumalted_list = [categs[4]]
    accumalted_list.extend(labels[12:])

    return Lottery649(
                winning_numbers = [int(tag.string) for tag in soup.find_all(id=re.compile("Lotto649Control_history_dlQuery_SNo[0-7]_0"))],
                special_number = int(soup.find(id="Lotto649Control_history_dlQuery_No7_0").string),
                item = LotteryItem.Lottery649,
                period = soup.find(id="Lotto649Control_history_dlQuery_L649_DrawTerm_0").string,
                drawing_date = soup.find(id="Lotto649Control_history_dlQuery_L649_DDate_0").string,
                due_date = soup.find(id="Lotto649Control_history_dlQuery_L649_EDate_0").string,
                sales_money = soup.find(id="Lotto649Control_history_dlQuery_L649_SellAmount_0").string,
                total_prize = soup.find(id="Lotto649Control_history_dlQuery_Total_0").string,
                prizes = __generate_lottery649_prizes(winners, prize_money_list, accumalted_list)
            )

def scrape_lottery649_by_seq(seq):
    pass

def scrape_lottery649_by_date(date):
    pass

if __name__ == "__main__":
    ticket = LotteryTicket(LotteryItem.Lottery649, "109/11/27", "109/11/27", 50, [1, 2, 3, 4, 5, 6])
    print("You buy a ticket", ticket.__dict__)

    last_lotto = scrape_lottery649_lastest()
    print("\nLast Lottery649 is", last_lotto.__dict__)
