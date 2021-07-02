
import calendar
from calendar import weekday, monthrange, SUNDAY 
import datetime 

from menu import ledgerMenu
# print(calendar.MONDAY)
# # 0 is Monda
# print(weekday(2021,7,1))
# print(monthrange(2021, 7)[2])

# print([weekday(2021, 7, d) for d in range(*monthrange(2021, 7))]) 
# print([weekday(2021, 7, d) for d in range(1,32)]) 


print(ledgerMenu.getLedger("202107"))