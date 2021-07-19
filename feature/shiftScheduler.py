import random

class ShiftScheduler:
    mans = ['Feng','CO','YO','文B']
    def randomShift():
        luckyMan = ShiftScheduler.mans[random.randint(0,3)]
        return luckyMan
