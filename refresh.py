




from subprocess import call,check_output
import os
import time 


password='root'
cmd_list = [
        'sudo apt update',
        'sudo apt upgrade -y',
        'sudo kill -9 -1', 
        "apt autoclean",
        "apt autoremove"
        
        ]

for cmd in cmd_list : 
    print("@@@@@@@@" , ' '.join(cmd.split()[1:]) , "@@@@@@@@")
    time.sleep(1)
    call('echo {} | sudo -S {}'.format(password, cmd), shell=True)
    os.system('clear')
    
