import requests
from bs4 import BeautifulSoup
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

    def _atoi(self, str_with_comma):
        return int(str_with_comma.replace(',', ''))

    def _check_lottery(self, lottery):
        return True

    def _parse_lottery(self, table_tag):
        rows = table_tag.find_all('tr')

        cols = rows[1].find_all('span')
        period = cols[0].string
        drawing_date = cols[2].string
        due_date = cols[3].string
        sales_money = self._atoi(cols[4].string)
        total_prize = self._atoi(cols[5].string)

        cols = rows[4].find_all('span')
        winning_numbers = [int(num.string) for num in cols[0:6]]
        special_number = int(cols[7].string)

        winner_list = [self._atoi(winner.string)
                       for winner in rows[8].find_all('span')[1:]]
        prize_money_list = [self._atoi(prize.string)
                            for prize in rows[9].find_all('span')[1:]]
        next_prize_money_list = [self._atoi(n.string)
                                 for n in rows[10].find_all('span')[1:]]
        zip_list = itertools.zip_longest(
            [(6, 0), (5, 1), (5, 0), (4, 1), (4, 0), (3, 1), (2, 1), (3, 0)],
            winner_list,
            prize_money_list,
            next_prize_money_list,
            fillvalue=None)
        prizes = {k: LotteryPrize(k, w, p, n) for (k, w, p, n) in zip_list}

        lottery = Lottery(period=period,
                          drawing_date=drawing_date,
                          due_date=due_date,
                          sales_money=sales_money,
                          total_prize=total_prize,
                          prizes=prizes,
                          winning_numbers=winning_numbers,
                          special_number=special_number)
        return lottery if self._check_lottery(lottery) else None

    def scrape_latest(self) -> Lottery:
        response = requests.get(self._url)
        soup = BeautifulSoup(response.text, "html.parser")
        table_tag = soup.find(
            'table', id='Lotto649Control_history_dlQuery').find('table')
        lottery = self._parse_lottery(table_tag)
        return lottery

    def scrape_by_month(self, year, month) -> List[Lottery]:
        # ASP.NET驗證資訊
        response = requests.get(self._url)
        soup = BeautifulSoup(response.text, "html.parser")
        view_state = soup.find(id='__VIEWSTATE').get('value')
        event_validation = soup.find(id='__EVENTVALIDATION').get('value')
        data = {
            '__VIEWSTATE': view_state,
            '__EVENTVALIDATION': event_validation,
            'Lotto649Control_history$dropYear': year,
            'Lotto649Control_history$dropMonth': month,
            'Lotto649Control_history$btnSubmit': '查詢'
        }

        response = requests.post(self._url, data=data)
        soup = BeautifulSoup(response.text, "html.parser")
        table_tags = soup.find(
            'table', id='Lotto649Control_history_dlQuery').find_all('table')
        lottery_list = [lottery for lottery in (self._parse_lottery(
            tag) for tag in table_tags) if lottery is not None]
        return lottery_list


class LotteryChecker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

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
    latest_lottery = scraper.scrape_latest()

    # buy a ticket
    my_ticket = LotteryTicket(
        '2020/11/22', '2020/11/23', [1, 2, 3, 4, 5, 6], '自選')

    # get prize
    checker = LotteryChecker()
    prize = checker.check(latest_lottery, my_ticket)

    print('Latest Date:', latest_lottery.drawing_date)
    if prize:
        print('Prize:', prize.title, prize.prize_money, '元')
    else:
        print('GG!')

    # lottery of one month
    month_lottery = scraper.scrape_by_month(110, 1)
    for lottery in month_lottery:
        print('Date:', lottery.drawing_date)
        print('Winning numbers:', lottery.winning_numbers,
              'special:', lottery.special_number)
