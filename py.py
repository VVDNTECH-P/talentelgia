list1 = {'user1' : [1 , 2 , 3] , 'user2' : [5 , 6 , 7]}

card = 1

for key , value  in list1.items() :

    if card == value[0] :
        print('valid user ')
        
        print("Your balance is " , value[2])
        
        