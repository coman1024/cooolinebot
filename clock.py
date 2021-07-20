from apscheduler.schedulers.blocking import BlockingScheduler

import urllib.request
import urllib.error
import os


from config import initConfig
from linebot.models import FlexSendMessage
from config.lineBotConfig import LinbotConfig
from menu import (
    notifyMenu,
    rewMenu,
    shiftMenu
)

initConfig.initialize()
scheduler = BlockingScheduler()
url = os.getenv('APP_URL')
print('start clock')

@scheduler.scheduled_job('interval',  minutes=21)
def wake_me_up_job():
    try:
        urllib.request.urlopen(url)
        print('Wake me up when september ends')
    except urllib.error.URLError as e:
        print('Request to url:', url, 'error.')
        print('Reason:', e.reason)
    except:
        print('Invalid url:', url)



@scheduler.scheduled_job('cron', day_of_week='tue,fri', hour='22', minute='10', timezone='Asia/Taipei')
def lottery649_drawing_job():
    print("開始通知")
    subscriber_ids = notifyMenu.getIdAll()
    if (len(subscriber_ids) == 0):
        print("沒有通知")
        return "OK"

    for id in subscriber_ids:
        try:
            line_bot_api = LinbotConfig.get_line_bot_api()
            line_bot_api.push_message(id[0],  FlexSendMessage(
                alt_text = "最新中獎號碼",
                contents = rewMenu.newestReward()
            ))
        except Exception as  e:
            continue   
    print('Notify done.')

@scheduler.scheduled_job('cron', day='20', hour='11', minute='30', timezone='Asia/Taipei')
def pickLotteryNumber_job():
    print("誰去買樂透")
    subscriber_ids = notifyMenu.getIdAll()
    if (len(subscriber_ids) == 0):
        print("沒有通知")
        return "OK"

    for id in subscriber_ids:
        try:
            line_bot_api = LinbotConfig.get_line_bot_api()
            line_bot_api.push_message(id[0],  FlexSendMessage(
                    alt_text = "誰去買樂透",
                    contents = shiftMenu.shift()
                ))
        except Exception as e:
            print(str(e))
            continue         

scheduler.start()
