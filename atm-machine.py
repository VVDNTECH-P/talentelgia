data={11111111 : ['user1',1111,100], 22222222 : ['user2',2222,200], 33333333 : ['user3',3333,300], 44444444 : ['user4',4444,400], 55555555 : ['user5',5555,500]}


def check():
    card_name = input('enter the name of card : ')
    try :
        if int(card_name) in data.keys() :   #agar user string enter karega voh integer mein convert nahi ho sakta that's why except block run
            print('valid user')
            print('User name is : ',data[int(card_name)][0])
            def pin():
                pin=input("Enter PIN Number: ")
                try:
                    if int(pin) in data[int(card_name)]:  
                        print('valid pin')
                        print('User pin is : ',data[int(card_name)][1])
                        print('User balance is : ',data[int(card_name)][2])
                        terminate= input('if you want to terminate the transaction write exit ')
                        if terminate.upper() == 'EXIT':
                            print("thanks for using our service ")
                        else:
                            check()    
                    else :
                        print('Invalid pin')
                        check()
                except:
                    print('pin number must be integers')  
                    check()

            pin()
        else :
            print('else block,inavlid card number')
            check()
    except:
        print('except,Card number must be integers')
        check()

check()
