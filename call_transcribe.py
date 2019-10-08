from test import DictatorSlave
import keyboard,time


def change_state():
    a.flag_call = 1


while True:
    cont = input("Do you want to Start this application ? Y or N?\n").lower().strip()
    if cont[0] == 'y':
        a = DictatorSlave(0)
        while a.flag_call is 0:
            if input() == '*':
                change_state()
            if int(a.flag_call) is 1:
                print("started")
                a.incoming_call()
                print("Call Ended Successfully")
            elif input() == 'e' or 'E':
                exit()
            else:
                continue

    elif cont[0] == 'n':
        print("Transcriber Terminated.\n")
        exit()

    else:
        print("Wrong Input. Enter Again.\n")
        continue
