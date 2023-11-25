import os 
from time import sleep

#User Global 
cur_path = os.getcwd()
UserData = open(cur_path +"/UserData.txt","r")
UserDataR = UserData.readlines()
UserData.close()
login = None
#----------------------------------------------------------------------------------------------------

#Basket Global 
itembasket = {}
total_items = 0
total_discount = 0
total_price = 0

#----------------------------------------------------------------------------------------------------

# Logistic Global
itemlist_path = cur_path+"/ItemList.txt"
itemlist_file = open(itemlist_path, "r")

item_price = {}
Read_Item = itemlist_file.readlines()
for line in Read_Item:
  Item,Price = line.strip("\n").split(" ")
  item_price[Item] = int(Price)
itemList = list(item for item,price in item_price.items())
itemlist_file.close()
item_discount_rate = 0

#----------------------------------------------------------------------------------------------------
def get_user_balance(username):
  for user_info in UserDataR:
    nameLine,passLine,cashLine = user_info.split("\t")
    if username == nameLine:
      return float(cashLine.strip("\n"))
#----------------------------------------------------------------------------------------------------

def Register(Name,Password):
  for User in UserDataR:
    nameLine = User.split("\t")[0]
    if Name == nameLine:
      print("This Username has been used. Please user another Username.")
      return "Fail"
  Usage = f"{Name}\t{Password}\t0\n"
  with open(cur_path +"/UserData.txt","a") as WorkUser:
    WorkUser.write(Usage)
  return "Pass"

#----------------------------------------------------------------------------------------------------

def Login(Username,Password):
  global login
  for Set in UserDataR:
    nameLine = Set.split("\t")[0]
    passLine = Set.split("\t")[1]
    if Username == nameLine:
      if Password == passLine:
        login = Username
        sleep(2)
        print("Enjoy!")
        return "Pass"
      elif Password != passLine:
        return "FailPass"
  print("Please Register.")
  
#----------------------------------------------------------------------------------------------------

def shoppingcart(select,count):
    global itembasket
    if select in itemList:
        if select in itembasket:
            itembasket[select] += int(count)
        else:
            itembasket[select] = int(count)

#----------------------------------------------------------------------------------------------------

def calculation(username):
  global   total_items, total_price, total_discount
  print("="*40)
  print("{:<20}{:<10}{:10}".format("Item","Price","Amount"))

  for item,count in itembasket.items():
    Get_item_price = item_price[item]
    total_items += count
    total_price += Get_item_price * count
    print("{:<20} ${:<10} {:<10}".format(item, item_price[item], count))
    
  print("=" * 40)
  total_discount = 0.1 * total_price
  print("{:<30} ${:<10}".format("Discount", total_discount))
  print("=" * 40)
  total_amount = total_price - total_discount
  print("{:<30} ${:<10}".format("Total", total_amount))
  print("=" * 40)
  confirmation = input("type 'confirm' to place order:")
  if confirmation.lower() == 'confirm':
    user_balance = get_user_balance(username)
    
    if user_balance >= total_price - total_discount:
      new_balance = user_balance - (total_price - total_discount)
      for i, user_info in enumerate(UserDataR):
              nameLine, passLine, cashLine = user_info.split("\t")
              if username == nameLine:
                UserDataR[i] = f"{nameLine}\t{passLine}\t{new_balance}\n"
                with open(cur_path + "/UserData.txt", "w") as UserData:
                  UserData.writelines(UserDataR)
    else:
      return "NotEnough"

#----------------------------------------------------------------------------------------------------

def deposit_cash(username, amount):
  global UserDataR
  for i, user_info in enumerate(UserDataR):
    nameLine, passLine, cashLine = user_info.split("\t")
    if username == nameLine:
      new_cash = float(cashLine) + amount
      UserDataR[i] = f"{nameLine}\t{passLine}\t{new_cash}\n"
  print(UserDataR)
  with open(cur_path + "/UserData.txt", "w") as UserData:
    UserData.writelines(UserDataR)

#----------------------------------------------------------------------------------------------------
    
def main():
  Main = True
  global login,UserDataR,total_items, total_price,total_discount
  while Main:
    print("\nShopping System")
    UserData = open(cur_path +"/UserData.txt","r")
    UserDataUR = UserData.readlines()
    UserDataR = UserDataUR
    UserData.close()
    while True:
      print("\n Login page")
      Username = input("Please enter your username(leave space on username for register):")
      Password = input("Please enter your password:")
      if Username in "                                       ":
        Loginface = "FailId"
        break
      else:
        Loginface = Login(Username,Password)
        if Loginface == False:
          pass
        else:
          break
    if Loginface == "Pass":
      RunItem = True
      while RunItem:
        while True:
          try:
            itemAdd = input("Please enter your items/amount (separate with A space):")
            item,amount = itemAdd.split(" ")
            print(itemList)
            if item not in itemList:
              print("please enter exist item")
              pass
            else:
              shoppingcart(item,amount)
              
              print(itembasket)
              break
          except ValueError:
            print("Please left just one space")
        clientContinute = input("Do you want to stop shopping? (Y/N):")
        if clientContinute.upper() == "Y":
          break
        else:
          pass
      while True:
        calculated = calculation(login)
        if calculated == "NotEnough":
          clientdeposit = input("Do you want to deposit?(Y for deposit):")
          if clientdeposit.lower() == "y":
            deposit_amount = float(input("Enter the amount of deposit:"))
            deposit_cash(Username, deposit_amount)
            total_discount = 0
            total_price = 0
          else:
            print("You cash not enough for these items.\nPlease be right back later.")
            total_items = 0
            total_discount = 0
            total_price = 0
            login = None
            itembasket.clear() 
            break
        else:
          total_items = 0
          total_discount = 0
          total_price = 0
          login = None
          itembasket.clear()
          print("Sucessful Trading!")
          break
    else:
      if Loginface == "FailPass":
        print("Please enter password again")
      if Loginface == "FailId":
        while True:
          sleep(1)
          print("REGISTER PAGE")
          signame = input("Enter your Username:")
          sigpass = input("Enter your Password:")
          Registerface = Register(signame,sigpass)
          sleep(1)
          if Registerface == "Fail":
            print("Please enter infomation again!")
            pass
          elif Registerface == "Pass":
            print("\nSuccessful SIGIN!")
            break

  
if __name__ == "__main__":
  main()