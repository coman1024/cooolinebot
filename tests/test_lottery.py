import unittest
from feature.lottery import Lottery649, LotteryItem, LotteryTicket, LotteryPrize, lottery649_checker

class LotteryTest(unittest.TestCase):

    def setUp(self):
        self.lotto = Lottery649(
            winning_numbers=[1, 2, 3, 4, 5, 6],
            special_number=7,
            item=LotteryItem.Lottery649,
            period='109000103',
            drawing_date='109/11/27',
            due_date='110/03/02',
            sales_money='122,995,950',
            total_prize='343,555,754',
            prizes={
                (6, 0): LotteryPrize(title='頭獎', description='6個', winners='0', prize_money='0', next_prize_money='301,244,982'),
                (5, 1): LotteryPrize(title='貳獎', description='任5個＋特別號', winners='1', prize_money='2,105,917', next_prize_money='0'),
                (5, 0): LotteryPrize(title='參獎', description='任5個', winners='39', prize_money='58,151', next_prize_money='0'),
                (4, 1): LotteryPrize(title='肆獎', description='任4個＋特別號', winners='111', prize_money='13,134', next_prize_money='0'),
                (4, 0): LotteryPrize(title='伍獎', description='任4個', winners='2,099', prize_money='2,000', next_prize_money=None),
                (3, 1): LotteryPrize(title='陸獎', description='任3個＋特別號', winners='3,161', prize_money='1,000', next_prize_money=None),
                (2, 1): LotteryPrize(title='柒獎', description='任2個＋特別號', winners='33,588', prize_money='400', next_prize_money=None),
                (3, 0): LotteryPrize(title='普獎', description='任3個', winners='39,212', prize_money='400', next_prize_money=None)
            }
        )

        self.ticket = LotteryTicket(
            LotteryItem.Lottery649,
            "109/11/27",
            "109/11/27",
            50,
            [1, 2, 3, 4, 5, 6]
        )

    def tearDown(self):
        self.lotto = None

    def test_lottery649_checker(self):
        self.ticket.pick_numbers = [1, 2, 3, 4, 5, 6]
        self.assertEqual(lottery649_checker(self.lotto, self.ticket), self.lotto.prizes[(6, 0)])

        self.ticket.pick_numbers = [1, 2, 3, 4, 5, 7]
        self.assertEqual(lottery649_checker(self.lotto, self.ticket), self.lotto.prizes[(5, 1)])

        self.ticket.pick_numbers = [1, 2, 3, 4, 5, 11]
        self.assertEqual(lottery649_checker(self.lotto, self.ticket), self.lotto.prizes[(5, 0)])

        self.ticket.pick_numbers = [1, 2, 3, 4, 7, 11]
        self.assertEqual(lottery649_checker(self.lotto, self.ticket), self.lotto.prizes[(4, 1)])

        self.ticket.pick_numbers = [1, 2, 3, 4, 12, 11]
        self.assertEqual(lottery649_checker(self.lotto, self.ticket), self.lotto.prizes[(4, 0)])

        self.ticket.pick_numbers = [1, 2, 3, 7, 12, 11]
        self.assertEqual(lottery649_checker(self.lotto, self.ticket), self.lotto.prizes[(3, 1)])

        self.ticket.pick_numbers = [1, 2, 7, 13, 12, 11]
        self.assertEqual(lottery649_checker(self.lotto, self.ticket), self.lotto.prizes[(2, 1)])

        self.ticket.pick_numbers = [1, 2, 3, 13, 12, 11]
        self.assertEqual(lottery649_checker(self.lotto, self.ticket), self.lotto.prizes[(3, 0)])

        # (2, 0)
        self.ticket.pick_numbers = [1, 2, 14, 13, 12, 11]
        self.assertIsNone(lottery649_checker(self.lotto, self.ticket))
        
        # (1, 1)
        self.ticket.pick_numbers = [1, 7, 14, 13, 12, 11]
        self.assertIsNone(lottery649_checker(self.lotto, self.ticket))

        # (1, 0)
        self.ticket.pick_numbers = [1, 15, 14, 13, 12, 11]
        self.assertIsNone(lottery649_checker(self.lotto, self.ticket))

        # (0, 1)
        self.ticket.pick_numbers = [7, 15, 14, 13, 12, 11]
        self.assertIsNone(lottery649_checker(self.lotto, self.ticket))

        # (0, 0)
        self.ticket.pick_numbers = [16, 15, 14, 13, 12, 11]
        self.assertIsNone(lottery649_checker(self.lotto, self.ticket))

if __name__ == "__main__":
    unittest.main()