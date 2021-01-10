from ..data.lottery import Lottery, LotteryScraper, LotteryTicket, LotteryChecker
from ..messages.lottery_message import LotteryMessage
from linebot.models import FlexSendMessage
from feature.DBNumber import NumberTbl


class LotteryReply:
    def _get_tickets_by_date(self, date):
        tickets = [LotteryTicket(draw_date, draw_date, [int(number.strip()) for number in numbers.split(',')],
                                 '自選' if lottery_type == 0 else '電選')
                   for draw_date, numbers, lottery_type in NumberTbl.findNm(None, date, None)]
        return tickets

    def _get_tickets_by_month(self, year, month):
        pass

    def _generate_ticket_prize_pair_list(self, lottery, tickets):
        return [(ticket, LotteryChecker().check(lottery, ticket))
                for ticket in tickets if lottery.drawing_date == ticket.drawing_date]

    def get_reply_message(self, type):
        if type == 'get_latest':
            lottery = LotteryScraper().scrape_latest()
            tickets = self._get_tickets_by_date(lottery.drawing_date) or []

            pairs = self._generate_ticket_prize_pair_list(lottery, tickets)
            contents = LotteryMessage(lottery, pairs).get_message()

            return FlexSendMessage(alt_text='最新中獎號碼',
                                   contents=contents)

    def get_reply_message_for_month(self, year, month):
        lottery_list = LotteryScraper().scrape_by_month(year, month)
        tickets = self._get_tickets_by_month(year, month) or []

        contents = []
        for lottery in lottery_list:
            pairs = self._generate_ticket_prize_pair_list(lottery, tickets)
            content = LotteryMessage(lottery, pairs).get_message()
            contents.append(content)

        alt_text = str(year) + '/' + str(month) + '中獎號碼'
        message = FlexSendMessage(
            alt_text=alt_text,
            contents={'type': 'carousel',
                      'contents': contents
                      })

        return message
