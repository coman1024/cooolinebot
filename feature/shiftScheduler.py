import random

class ShiftScheduler:
    mans = ['Feng','CO','YO','文B']
    def randomShift():
        luckyMan = ShiftScheduler.mans[random.randint(0,3)]
        print(luckyMan)
        return luckyMan

class ShiftInfo:
    def __init__(self, shiftDate: str, luckyMan: str):
        self.shiftDate = shiftDate
        self.luckyMan = luckyMan





