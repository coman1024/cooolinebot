import requests
from bs4 import BeautifulSoup
import re
from enum import Enum
from typing import Dict, List, Tuple

class LotteryPrize:
    def __init__(self, title: str, description: str, winners: int, prize_money: int, next_prize_money: int):
        self. title = title
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
    print("Lottery649 numbers are:", lotto.winning_numbers, "and", lotto.special_number)
    print("Your picking numbers are:", ticket.pick_numbers)

    winning_tuple = (winning_count, win_special_number)
    prize = lotto.prizes[winning_tuple] if winning_tuple in lotto.prizes else None
    if prize:
        print("You win the ", prize.__dict__)
    else:
        print("LOSE QQQQQ")
    #print("")

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
    lotto = Lottery649(
        [45, 29, 36, 5, 38, 44],
        23,
        item = LotteryItem.Lottery649,
        period = "109000102",
        drawing_date = "109/11/24",
        due_date = "110/02/24",
        sales_money = 120024550, 
        total_prize = 318009096,
        prizes = {
            (6, 0): LotteryPrize("jackpot", "6+0", 0, 0, 274678022),
            (5, 1): LotteryPrize("2nd prize", "5+1", 3, 2028973, 0),
            (5, 0): LotteryPrize("3rd prize", "5+0", 42, 56439, 0),
            (4, 1): LotteryPrize("4th prize", "4+1", 110, 13853, 0),
            (4, 0): LotteryPrize("5th prize", "4+0", 1949, 2000, 0),
            (3, 1): LotteryPrize("6th prize", "3+1", 2765, 1000, 0),
            (2, 1): LotteryPrize("7th prize", "2+1", 30161, 400, 0),
            (3, 0): LotteryPrize("8th prize", "3+0", 36556, 400, 0)
        }
    )

    tickets = [
        LotteryTicket(LotteryItem.Lottery649, "109/11/22", "109/11/24", 50, [45, 29, 36, 5, 38, 44]),
        LotteryTicket(LotteryItem.Lottery649, "109/11/22", "109/11/24", 50, [23, 29, 36, 5, 38, 44]),
        LotteryTicket(LotteryItem.Lottery649, "109/11/22", "109/11/24", 50, [45, 456, 36, 5, 123, 44]),
        LotteryTicket(LotteryItem.Lottery649, "109/11/22", "109/11/24", 50, [45, 100, 101, 102, 38, 44]),
        LotteryTicket(LotteryItem.Lottery649, "109/11/22", "109/11/24", 50, [45, 100, 101, 102, 29, 44]),
        LotteryTicket(LotteryItem.Lottery649, "109/11/22", "109/11/24", 50, [100, 101, 102, 103, 104, 105])
    ]
    
    for ticket in tickets:
        lottery649_checker(lotto, ticket)
        print("")
