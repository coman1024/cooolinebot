import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Tuple
import itertools


class LotteryPrize:
    def __init__(self, item: Tuple[int, int], winners: int, prize_money: int, next_prize_money: int):
        items = {
            (6, 0): ("頭獎", "6個"),
            (5, 1): ("貳獎", "任5個＋特別號"),
            (5, 0): ("參獎", "任5個"),
            (4, 1): ("肆獎", "任4個＋特別號"),
            (4, 0): ("伍獎", "任4個"),
            (3, 1): ("陸獎", "任3個＋特別號"),
            (2, 1): ("柒獎", "任2個＋特別號"),
            (3, 0): ("普獎", "任3個"),
        }
        self.item = item
        self.title = items[item][0]
        self.rule = items[item][1]
        self.winners = winners
        self.prize_money = prize_money
        self.next_prize_money = next_prize_money


class LotteryTicket:
    def __init__(self, purchase_date: str, drawing_date: str, pick_numbers: List[int], picker: str):
        self.purchase_date = purchase_date
        self.drawing_date = drawing_date
        self.prize = 50
        self.picker = picker
        self.pick_numbers = pick_numbers


class Lottery:
    def __init__(
            self, period: str, drawing_date: str, due_date: str, sales_money: int, total_prize: int,
            prizes: Dict[Tuple[int, int], LotteryPrize], winning_numbers: List[int], special_number: int):
        self.period = period
        self.drawing_date = drawing_date
        self.due_date = due_date
        self.sales_money = sales_money
        self.total_prize = total_prize
        self.prizes = prizes
        self.winning_numbers = winning_numbers
        self.special_number = special_number


class LotteryScraper():
    def __init__(self):
        self._url = "https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx"
        self._response = requests.get(self._url)
        self._soup = BeautifulSoup(self._response.text, "html.parser")

    def _scrape_by_index(self, index):
        categs = [tag.string for tag in self._soup.find_all(id=re.compile(
            f"Lotto649Control_history_dlQuery_L649_Categ[ABC][345]_{index}"))]
        labels = [tag.string for tag in self._soup.find_all(
            id=re.compile(f"Lotto649Control_history_dlQuery_Label[0-9]+_{index}"))]

        winners = []
        prize_money_list = []
        accumalted_list = []
        if index % 2 == 0:
            winners.extend(categs[0:3])
            winners.extend(labels[0:5])

            prize_money_list.extend(categs[3])
            prize_money_list.extend(labels[5:12])

            # accumalted_list.extend(categs[4])
            # accumalted_list.extend(labels[12:])
        else:
            winners.extend(categs[0])
            winners.extend(labels[0:6])

            prize_money_list.extend(categs[1])
            prize_money_list.extend(labels[5:13])

            # accumalted_list.extend(categs[2])
            # accumalted_list.extend(labels[13:])

        return Lottery(
            period=self._soup.find(
                id=f"Lotto649Control_history_dlQuery_L649_DrawTerm_{index}").string,
            drawing_date=self._soup.find(
                id=f"Lotto649Control_history_dlQuery_L649_DDate_{index}").string,
            due_date=self._soup.find(
                id=f"Lotto649Control_history_dlQuery_L649_EDate_{index}").string,
            sales_money=self._soup.find(
                id=f"Lotto649Control_history_dlQuery_L649_SellAmount_{index}").string,
            total_prize=self._soup.find(
                id=f"Lotto649Control_history_dlQuery_Total_{index}").string,
            prizes={k: LotteryPrize(k, w, p, n) for (k, w, p, n) in itertools.zip_longest(
                [(6, 0), (5, 1), (5, 0), (4, 1), (4, 0), (3, 1), (2, 1), (3, 0)], winners, prize_money_list, accumalted_list, fillvalue=None)},
            winning_numbers=[int(tag.string) for tag in self._soup.find_all(
                id=re.compile(f"Lotto649Control_history_dlQuery_No[1-6]_{index}"))],
            special_number=int(self._soup.find(
                id=f"Lotto649Control_history_dlQuery_No7_{index}").string),
        )

    def scrape_last_one(self):
        return self._scrape_by_index(0)

    def scrape_by_date(self, date):
        drawing_date_list = [tag.string for tag in self._soup.find_all(
            id=re.compile(f"Lotto649Control_history_dlQuery_L649_DDate_[0-9]"))]

        targetIdx = 99
        for idx, item in enumerate(drawing_date_list):
            if date == item:
                targetIdx = idx
                break
        if (targetIdx == 99):
            raise RuntimeError("找不到開獎日期")

        return self._scrape_by_index(targetIdx)

    def scrape_by_seq(self, seq):
        drawing_seq_list = [tag.string for tag in self._soup.find_all(
            id=re.compile(f"Lotto649Control_history_dlQuery_L649_DrawTerm_[0-9]"))]
        targetIdx = 99
        for idx, item in enumerate(drawing_seq_list):
            if seq == item:
                targetIdx = idx
                break
        if (targetIdx == 99):
            raise RuntimeError("找不到開獎期數")

        return self._scrape_by_index(targetIdx)


class LotteryChecker:
    def __init__(self):
        pass

    def check(self, lotto: Lottery, ticket: LotteryTicket) -> LotteryPrize:
        winning_count = len(
            set(lotto.winning_numbers).intersection(set(ticket.pick_numbers)))
        win_special_number = lotto.special_number in ticket.pick_numbers

        winning_tuple = (winning_count, win_special_number)
        prize = lotto.prizes.get(winning_tuple, None)
        return prize


if __name__ == "__main__":
    # lottery scraper
    scraper = LotteryScraper()
    last_lottery = scraper.scrape_last_one()

    # buy a ticket
    my_ticket = LotteryTicket(
        '2020/11/22', '2020/11/23', [1, 2, 3, 4, 5, 6], '自選')

    # get prize
    checker = LotteryChecker()
    prize = checker.check(last_lottery, my_ticket)

    if prize:
        print('Prize:', prize.title, prize.prize_money, '元')
    else:
        print('GG!')
