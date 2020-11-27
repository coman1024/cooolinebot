import requests
from bs4 import BeautifulSoup
import re
from enum import Enum
from typing import Dict, List

class LotteryPrize:
    def __init__(self, winning_rule: str, winning_bets: int, prize_money: int, next_prize_money: int):
        self.winning_rule = winning_rule
        self.winning_bets = winning_bets
        self.prize_money = prize_money
        self.next_prize_money = next_prize_money

class LotteryItem(Enum):
    Lottery649 = "lottery649"

class Lottery:
    def __init__(self, item: LotteryItem, period: str, drawing_date: str, due_date: str, sales_money: int, total_prize: int, prizes: Dict[str, LotteryPrize]):
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
    print("Lottery649 numbers are:", lotto.winning_numbers, " and", lotto.special_number)
    print("Your picking numbers are:", ticket.pick_numbers)
    prize_dict = {
        (6, 0): "jackpot",
        (5, 1): "2nd_prize",
        (5, 0): "3rd_prize",
        (4, 1): "4th_prize",
        (4, 0): "5th_prize",
        (3, 1): "6th_prize",
        (2, 1): "7th_prize",
        (3, 0): "8th_prize"
    }
    winning_tuple = (winning_count, win_special_number)
    prize_money = 0
    if (winning_tuple in prize_dict):
        prize = prize_dict[winning_tuple]
        if (prize in lotto.prizes):
            prize_money = lotto.prizes[prize]
    else:
        prize = "LOSE QQQQQ"

    print("Result:", prize, " prize money:", prize_money)

def scrape_lottery649_lastest():
    response = requests.get("https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx")
    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.find_all(id=re.compile("Lotto649Control_history_dlQuery_SNo[0-7]_0"))
    winning_numbers = [tag.string for tag in tags]
    special_number = soup.find(id="Lotto649Control_history_dlQuery_No7_0").string
    print("Winning numbers: ", winning_numbers, "special:", special_number)    

def scrape_lottery649_by_seq(seq):
    pass

def scrape_lottery649_by_date(date):
    pass

if __name__ == "__main__":
    lotto = Lottery649([1,2,3,4,5,7], 9, item=LotteryItem.Lottery649, period="109000102", drawing_date="109/11/24", due_date="110/02/24", sales_money=120024550, total_prize=318009096, prizes={"jackpot": 274678022, "second_prize": 2028973})
    ticket = LotteryTicket(LotteryItem.Lottery649, "109/11/22", "109/11/24", 50, [1,2,3,4,7,5])
    lottery649_checker(lotto, ticket)