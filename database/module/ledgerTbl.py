
class Ledger:
    
    def __init__(self, owner: str, amount: int, payDate: str, createUser: str, *createDate: str):
        self.owner = owner
        self.amount = amount
        self.payDate = payDate 
        self.createUser = createUser
        self.createDate = createDate