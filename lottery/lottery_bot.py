from .reply.help_reply import HelpReply
from .reply.lottery_reply import LotteryReply
from .data.lottery import LotteryChecker


class LotteryBot:
    def __init__(self):
        self.lottery_checker = LotteryChecker()

    def get_reply_instance(self, type):
        if type == 'Lottery':
            return LotteryReply(self.lottery_checker)
        elif type == 'Help':
            return HelpReply()
