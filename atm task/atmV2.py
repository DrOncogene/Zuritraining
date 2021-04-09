import random, json

# my database will be a dictionary of dictionaries with account numbers as the keys
# rather than a dictionary of lists as used in the lecture
# require acct number and password to login
# account numbers are unique
# persist the credentials in to a db.txt file an object

users_db = {}

# open the db and load all available accounts
with open('db.txt') as database:
  content = database.read()
  if content != '':  
    users_db = json.loads(content)

def init():
  print('================ Welcome to NASBank ================')
  print('1. Login       2. Register')
  selectedOption = int(input('Choose and option to start: \n'))

  if selectedOption == 1:
    login()
  elif selectedOption == 2:
    register()
  else:
    print('Invalid option selected')
    init()


def register():
  print('Register for an account with us today!')
  # variable to check if account number is unique i.e. doesn't exist already
  exists = True
  first_name = input('Enter your first name: \n')
  last_name = input('Enter your last name: \n')
  email = input('Enter a valid email address: \n')
  password = input('Create a password: \n')
  while exists:
    account_number = str(random.randrange(1111111111, 9999999999))
    try:
      # try to get the user using the account number generated as key
      user = users_db[account_number]
    # if trying to get the user raises a keyerror, i.e. does not exist
    # set exists to false to break the loop
    except KeyError:
      exists = False

  # create a new user dict
  new_user = {
    'first': first_name,
    'last': last_name,
    'email': email,
    'password': password,
    'balance': 0,
    'complaints': []
  }
  # save it to the db using the account number as the key
  users_db[account_number] = new_user
  # save the db to the db.txt file
  save_to_db()
  print('Registration successful!')
  print(f'Your account number is {account_number}')
  init()


def login():
  print('========= Login =========')
  userFound = False
  while userFound == False:
    try:
      # get credentials and try to get the user from the db
      account_number = input('Enter your account number: \n')
      password = input('Enter password \n')
      user = users_db[account_number]
      if user and user['password'] == password:
        # set to true to break loop is credentials are correct
        userFound = True
      else:
        print('Invalid email or password')
    except KeyError:
      print(f"Account '{account_number}' does not exist")
  # get the first and last name and capitalize them
  name = f"{user['first'].capitalize()} {user['last'].capitalize()}"
  print(f"Welcome {name}!")
  # print the current user balance
  print(f'Your balance: #{user["balance"]}')
  bankOperations(account_number)


def bankOperations(account):
  print('1. Withdraw cash     2. Deposit cash     3. Transfer     4. Complaint      5. Cancel')
  selectedOption = int(input('What would you like to do? \n'))
  if selectedOption == 1:
    withdraw(account)
  elif selectedOption == 2:
    deposit(account)
  elif selectedOption == 3:
    transfer(account)
  elif selectedOption == 4:
    complaint(account)
  elif selectedOption == 5:
    exit()
  else:
    print('Invalid option selected')
    bankOperations(account)


def withdraw(account):
  user = users_db[account]
  print(f'Your balance: #{user["balance"]}')
  amount = int(input('Enter an amount to withdraw: \n'))
  # check if there are enough funds in the account
  if amount <= user['balance']:
    if amount > 0:
      user['balance'] -= amount
      users_db[account] = user
      save_to_db()
      print('Take your cash, thank you for banking with us')
      print(f'Your new balance is #{user["balance"]}')
    else:
      print('No amount entered')
      withdraw(account)
    bankOperations(account)
  else:
    print('Insufficient balance')
    withdraw(account)  
  bankOperations(account)
     


def deposit(account):
  user = users_db[account]
  print(f'Your balance: #{user["balance"]}')
  amount = int(input('Enter an amount to deposit: \n'))
  if amount > 0:
    user['balance'] += amount
    users_db[account] = user
    save_to_db()
    print(f'#{amount} successfully added, thank you for banking with us')
    print(f'Your new balance is #{user["balance"]}')
  else:
    print('No amount entered')
    deposit(account)
  bankOperations(account)

# the to parameter is set to a default to allow it to be called above with one argument
def transfer(account, to=''):
  sender = users_db[account]
  to = input('Enter recipient account number: \n')
  try:
    recipient = users_db[to]
  except KeyError:
    print(f'Account {to} does not exist')
    transfer(account)
  recipient_name = f"{recipient['first'].capitalize()} {recipient['last'].capitalize()}"
  amount = int(input('Enter amount to transfer: \n'))
  confirm = input(f'Transfer {amount} to {recipient_name} y/n \n')
  if confirm == 'y':
    if amount <= sender['balance']:
      sender['balance'] -= amount
      recipient['balance'] += amount
      users_db[account] = sender
      users_db[to] = recipient
      save_to_db()
      print('Transfer successful')
    else:
      print('Insufficient balance')
      transfer(account)
  elif confirm == 'n':
      print('Transfer cancelled')
      bankOperations(account)
  else:
    print('Invalid option entered')
    transfer(account)
  bankOperations(account)


def complaint(account):
  user = users_db[account]
  complaint = input('We are very sorry for any incoveniencies. What is your complaint? \n')
  user['complaints'].append(complaint)
  users_db[account] = user
  save_to_db()
  print('Complaint submitted. We will contact you soon')
  bankOperations(account)


def save_to_db():
  with open('db.txt', 'w') as usersDB:
    print(json.dumps(users_db, indent=4), file=usersDB)


if __name__ == '__main__':
  init()