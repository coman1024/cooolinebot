from ..data.lottery import LotteryScraper, LotteryTicket, LotteryChecker
from ..messages.lotteryMessage import LotteryMessage
from linebot.models import FlexSendMessage


class LotteryReply:
    def __init__(self, lottery_checker):
        self.checker = lottery_checker

    def _get_tickets(self):
        pass

    def get_reply_message(self, type):
        if type == 'get_last_one':
            last_lottery = LotteryScraper().scrape_last_one()
            tickets = self._get_tickets() or []

            message = FlexSendMessage(alt_text="最新中獎號碼")

            if tickets:
                message.contents = {
                    'type': 'carousel',
                    'contents': [LotteryMessage(last_lottery, self.checker.check(
                        last_lottery, ticket), ticket).get_message() for ticket in tickets]
                }
            else:
                message.contents = LotteryMessage(
                    last_lottery, None, None).get_message()

            return message

        elif type == 'get_last_month':
            pass
