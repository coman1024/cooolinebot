import crawler.crawler



Crawler = crawler.crawler.Crawler()
targetDate = input("請輸入日期: ") #109/10/30
goldNumber = Crawler.findByDate(targetDate)
print ("得獎號碼：" + goldNumber)