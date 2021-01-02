from ..data.lottery import Lottery, LotteryPrize, LotteryTicket
from ..util import formatNumberList
from typing import List, Tuple


class LotteryMessage:
    def __init__(self, lottery: Lottery, ticket_prize_pairs: List[Tuple[LotteryTicket, LotteryPrize]]):
        self.lottery = lottery
        self.pairs = ticket_prize_pairs or []

    def _prize_message(self, prize: LotteryPrize):
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "結果：",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": prize.title + ' $' + str(prize.prize_money) if prize else '槓龜',
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                }
            ]
        }

    def _ticket_message(self, ticket: LotteryTicket):
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "text": "你的號碼："
                },
                {
                    "type": "text",
                    "text": '(' + ticket.picker + ') ' + formatNumberList(ticket.pick_numbers) if ticket else '票勒',
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                }
            ]
        }

    def get_message(self):
        message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": self.lottery.drawing_date,
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "中獎號碼：",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 0
                                    },
                                    {
                                        "type": "text",
                                        "text": formatNumberList(self.lottery.winning_numbers),
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "特別號：",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 0
                                    },
                                    {
                                        "type": "text",
                                        "text": str(self.lottery.special_number),
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }

        contents = message['body']['contents']
        for (ticket, prize) in self.pairs:
            contents.append({
                "type": "separator",
                "margin": "xxl"
            })
            contents.append(self._ticket_message(ticket))
            contents.append(self._prize_message(prize))

        if not self.pairs:
            contents.append(self._ticket_message(None))

        return message
