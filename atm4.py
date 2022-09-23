
data = {11111: {'user': 'user1', 'pin': 1111, 'balance': 10000},
        22222: {'user': 'user2', 'pin': 2222, 'balance': 20000},
        33333: {'user': 'user3', 'pin': 3333, 'balance': 30000},
        44444: {'user': 'user4', 'pin': 4444, 'balance': 40000},
        55555: {'user': 'user5', 'pin': 5555, 'balance': 50000}
        }
print('\n-------------------------  WELCOME TO ATM  -----------------------------\n')
def check():
    try:
        card_name = input('Please enter your card number :: ')
        print(card_name)
        if int(card_name) in data:
            print("Card Holder's name is :: ",data[int(card_name)]['user'])
            count = 0
            while count <= 3:
                pin = input("Enter your PIN Number :: ")
                try:
                    if int(pin) == data[int(card_name)]['pin']:
                        print("1-Balance Enquiry")
                        print("2-Withdraw")
                        choice = int(input('Please choose transactions :: '))
                        if choice == 1:
                            print("User's Account balance is : ",data[int(card_name)]['balance'])
                        if choice == 2:
                            w = int(input("Enter withdraw amount: "))
                            b = data[int(card_name)]['balance']
                            if w < b :
                                print("Please take your amount:", w)
                                b = b-w
                                print('User remaining balance is : ',b)
                            if w >=5000 :
                                print("withdraw amount should be less than 5000")  
                                check()  
                        terminate = input('if you want to terminate the transaction write exit ')
                        if terminate.upper() == 'EXIT':
                            print("thanks for using our service ")
                            break
                        else:
                            check()
                    else:
                        print('Invalid pin')
                        count += 1
                except:
                    print('pin number must be integers')
                    count += 1
            if (count == 4):
                print('4 UNSUCCESFUL PIN ATTEMPTS, EXITING')
        else:
            print('else block,inavlid card number')
            check()
    except:
        print('except,Card number must be integers')
        check()


check()
