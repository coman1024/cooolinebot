import unittest
from lottery.data.lottery import Lottery, LotteryChecker, LotteryPrize, LotteryTicket, LotteryScraper


class LotteryCheckerTest(unittest.TestCase):

    def setUp(self):
        self.lottery = Lottery(
            period='109000111',
            drawing_date='109/12/25',
            due_date='110/03/29',
            sales_money='98,968,150',
            total_prize='121,233,362',
            prizes={
                (6, 0): LotteryPrize((6, 0), winners='0', prize_money='0', next_prize_money='301,244,982'),
                (5, 1): LotteryPrize((5, 1), winners='1', prize_money='2,105,917', next_prize_money='0'),
                (5, 0): LotteryPrize((5, 0), winners='39', prize_money='58,151', next_prize_money='0'),
                (4, 1): LotteryPrize((4, 1), winners='111', prize_money='13,134', next_prize_money='0'),
                (4, 0): LotteryPrize((4, 0), winners='2,099', prize_money='2,000', next_prize_money=None),
                (3, 1): LotteryPrize((3, 1), winners='33,588', prize_money='400', next_prize_money=None),
                (2, 1): LotteryPrize((2, 1), winners='3,161', prize_money='1,000', next_prize_money=None),
                (3, 0): LotteryPrize((3, 0), winners='39,212', prize_money='400', next_prize_money=None)
            },
            winning_numbers=[1, 2, 3, 4, 5, 6],
            special_number=7
        )

        self.ticket = LotteryTicket(
            purchase_date="109/11/27",
            drawing_date="109/11/27",
            pick_numbers=[1, 2, 3, 4, 5, 6],
            picker='自選'
        )

    def tearDown(self):
        self.lottery = None

    def test_lottery_checker(self):
        self.ticket.pick_numbers = [1, 2, 3, 4, 5, 6]
        self.assertEqual(LotteryChecker().check(
            self.lottery, self.ticket), self.lottery.prizes[(6, 0)])

        self.ticket.pick_numbers = [1, 2, 3, 4, 5, 7]
        self.assertEqual(LotteryChecker().check(
            self.lottery, self.ticket), self.lottery.prizes[(5, 1)])

        self.ticket.pick_numbers = [1, 2, 3, 4, 5, 11]
        self.assertEqual(LotteryChecker().check(
            self.lottery, self.ticket), self.lottery.prizes[(5, 0)])

        self.ticket.pick_numbers = [1, 2, 3, 4, 7, 11]
        self.assertEqual(LotteryChecker().check(
            self.lottery, self.ticket), self.lottery.prizes[(4, 1)])

        self.ticket.pick_numbers = [1, 2, 3, 4, 12, 11]
        self.assertEqual(LotteryChecker().check(
            self.lottery, self.ticket), self.lottery.prizes[(4, 0)])

        self.ticket.pick_numbers = [1, 2, 3, 7, 12, 11]
        self.assertEqual(LotteryChecker().check(
            self.lottery, self.ticket), self.lottery.prizes[(3, 1)])

        self.ticket.pick_numbers = [1, 2, 7, 13, 12, 11]
        self.assertEqual(LotteryChecker().check(
            self.lottery, self.ticket), self.lottery.prizes[(2, 1)])

        self.ticket.pick_numbers = [1, 2, 3, 13, 12, 11]
        self.assertEqual(LotteryChecker().check(
            self.lottery, self.ticket), self.lottery.prizes[(3, 0)])

        # (2, 0)
        self.ticket.pick_numbers = [1, 2, 14, 13, 12, 11]
        self.assertIsNone(LotteryChecker().check(self.lottery, self.ticket))

        # (1, 1)
        self.ticket.pick_numbers = [1, 7, 14, 13, 12, 11]
        self.assertIsNone(LotteryChecker().check(self.lottery, self.ticket))

        # (1, 0)
        self.ticket.pick_numbers = [1, 15, 14, 13, 12, 11]
        self.assertIsNone(LotteryChecker().check(self.lottery, self.ticket))

        # (0, 1)
        self.ticket.pick_numbers = [7, 15, 14, 13, 12, 11]
        self.assertIsNone(LotteryChecker().check(self.lottery, self.ticket))

        # (0, 0)
        self.ticket.pick_numbers = [16, 15, 14, 13, 12, 11]
        self.assertIsNone(LotteryChecker().check(self.lottery, self.ticket))


class LotteryScraperTest(unittest.TestCase):
    def test_scrape_latest(self):
        scraper = LotteryScraper()
        lottery = scraper.scrape_latest()
        self.assertIsInstance(lottery, Lottery)
        self.assertIsInstance(lottery.prizes, dict)
        self.assertEqual(len(lottery.prizes), 8, 'Lottery prize should be 8')

    def test_scrape_month(self):
        scraper = LotteryScraper()
        lottery_list = scraper.scrape_by_month(109, 10)
        self.assertLessEqual(len(lottery_list), 9)
        self.assertGreaterEqual(len(lottery_list), 8)
        for lottery in lottery_list:
            self.assertIsInstance(lottery, Lottery)
            self.assertIsInstance(lottery.prizes, dict)
            self.assertEqual(len(lottery.prizes), 8,
                             'Lottery prize should be 8')
