class Budget():


  @staticmethod
  def transfer_fund(fro, to, amount: int) -> None:
    if (amount > 0) and (amount <= fro.balance):
      fro.balance -= amount
      to.balance += amount
    else:
      print('Invalid amount entered')

  def __init__(self, category: str, balance: int) -> None:
    self.category = category
    self.balance = balance

  def get_balance(self) -> int:
    return self.balance

  def add_fund(self, amount: int) -> None:
    self.balance += amount
  
  def withdraw_fund(self, amount: int) -> None:
    if amount <= self.balance:
      self.balance -= amount
    else:
      print('Invalid amount entered')

  def __str__(self):
    return f'Name: {self.category}, Balance {self.balance}'

# # code to test the class
# fashion = Budget('fashion', 0)
# sports = Budget('sports', 0)
# print(sports)
# print(fashion)
# sports.add_fund(1000)
# sports.withdraw_fund(200)
# sports.get_balance()
# print(sports)
# print(fashion)
# Budget.transfer_fund(sports, fashion, 450)
# print('====== After transfer from sports to fashion ======')
# print(sports)
# print(fashion)