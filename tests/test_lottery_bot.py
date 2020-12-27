import unittest
from lottery.lottery_bot import LotteryBot
from lottery.reply.help_reply import HelpReply
from lottery.reply.lottery_reply import LotteryReply


class LotteryBotTest(unittest.TestCase):
    def test_get_instance(self):
        bot = LotteryBot()
        self.assertIsInstance(bot.get_reply_instance('Lottery'), LotteryReply)
        self.assertIsInstance(bot.get_reply_instance('Help'), HelpReply)
