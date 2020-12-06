from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import urllib.error
import os

scheduler = BlockingScheduler()
url = os.getenv('APP_URL')

@scheduler.scheduled_job('interval', minutes=20)
def wake_me_up_job():
    try:
        urllib.request.urlopen(url)
        print('Wake me up when september ends')
    except urllib.error.URLError as e:
        print('Request to url:', url, 'error.')
        print('Reason:', e.reason)
    except:
        print('Invalid url:', url)

scheduler.start()