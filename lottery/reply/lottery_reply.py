from ..data.lottery import Lottery, LotteryScraper, LotteryTicket, LotteryChecker
from ..messages.lottery_message import LotteryMessage
from linebot.models import FlexSendMessage


class LotteryReply:
    def _mock_date_tickets(self, lottery):
        return [
            LotteryTicket(lottery.drawing_date, lottery.drawing_date, [
                          1, 2, 3, 4, 5, 6], '自選'),
            LotteryTicket(lottery.drawing_date, lottery.drawing_date, [
                          5, 14, 40, 44, 45, 32], '電選')
        ]

    def _get_tickets_by_date(self, date):
        pass

    def _mock_month_tickets(self, lottery_list):
        first_list = [LotteryTicket(lottery.drawing_date, lottery.drawing_date, [
            1, 2, 3, 4, 5, 6], '自選') for lottery in lottery_list]
        second_list = [LotteryTicket(lottery.drawing_date, lottery.drawing_date, [
            5, 14, 40, 44, 45, 32], '電選') for lottery in lottery_list]
        first_list.pop()
        first_list.pop(1)
        first_list.pop(2)
        second_list.pop()
        second_list.pop(1)
        return first_list + second_list

    def _get_tickets_by_month(self, year, month):
        pass

    def _generate_ticket_prize_pair_list(self, lottery: Lottery, tickets: LotteryTicket):
        return [(ticket, LotteryChecker().check(lottery, ticket))
                for ticket in tickets if lottery.drawing_date == ticket.drawing_date]

    def get_reply_message(self, type):
        if type == 'get_latest':
            lottery = LotteryScraper().scrape_latest()
            tickets = self._get_tickets_by_date(lottery.drawing_date) or []
            #tickets = self._mock_date_tickets(lottery)

            pairs = self._generate_ticket_prize_pair_list(lottery, tickets)
            contents = LotteryMessage(lottery, pairs).get_message()

            return FlexSendMessage(alt_text='最新中獎號碼',
                                   contents=contents)

    def get_reply_message_for_month(self, year, month):
        lottery_list = LotteryScraper().scrape_by_month(year, month)
        tickets = self._get_tickets_by_month(year, month) or []
        #tickets = self._mock_month_tickets(lottery_list) or []

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
