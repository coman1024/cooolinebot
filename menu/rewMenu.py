
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from feature.LotteryNumber import lotteryBot
from feature.RewardNumber import rewardBot

class reward1:
    label = "自選號碼最新兌獎"
    text = "reward1"
    def reward():
        lottery_bot = lotteryBot()
        reward_bot = rewardBot()
        glodNumber = lottery_bot.findNewNumber()
        return reward_bot.rewardFixedNum(glodNumber)

class reward2:
    label = "電選號碼對獎"
    text =  "reward2"
    def reward():
        return "還沒寫啦"
class reward3:
    label = "輸入號碼對獎"
    text = "reward3"
    def reward(targetNum):
        if(len(targetNum) == 0):
            return "請輸入 reward3 號碼,隔開(01,02,03,04,05,06)"
        try:
            return "還沒寫啦"
        except Exception as e:
            return str(e)     

menu = TemplateSendMessage(
    alt_text = '對獎功能選單',
    template = ButtonsTemplate(
        title = '你想要中什麼獎勒',
        text = '請選擇功能',
        actions = [
            MessageTemplateAction(
                label = reward1.label,
                text = reward1.text
            ),
            MessageTemplateAction(
                label = reward2.label,
                text = reward2.text
            ),
            MessageTemplateAction(
                label = reward3.label,
                text = reward3.text
            )
        ]
    )
)
