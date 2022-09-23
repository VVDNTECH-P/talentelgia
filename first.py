users={'One':[111111,1000,10000],
       'Two':[222222,2000,20000],
       'Three':[333333,3000,30000],
       'Four':[444444,4000,40000],
       'Five':[555555,5000,50000]}
def pin():
    for key,value in users.items() :
        pins=input("Enter Your PIN : ")
        if pins == str(value[1]) :
            print("Your Balance is : " , value[2])
            break
        else :
            print("Enter PIN again")
            pin()
            
def atm():
    card=input("Enter card details : ")
    for key,value in users.items() :
        if card == str(value[0]) :
            print("Hello " + key)
            pin()
            break
        else :
            print("Wrong Details")
            atm()
            
atm()
