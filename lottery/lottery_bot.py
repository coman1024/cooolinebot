from .reply.help_reply import HelpReply
from .reply.lottery_reply import LotteryReply


class LotteryBot:
    def get_reply_instance(self, type):
        if type == 'Lottery':
            return LotteryReply()
        elif type == 'Help':
            return HelpReply()
