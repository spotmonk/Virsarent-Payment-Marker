import pyautogui
import time
import pyperclip
import sys
from decimal import Decimal
from pdf import get_customers




def check_open():
    if  pyautogui.locateOnScreen('img/lastnameinput.png', confidence=.9) == None:
        vropen = pyautogui.locateOnScreen('img/VRopen.png', confidence=.9)
        if vropen != None:
            pyautogui.moveTo(vropen)
            pyautogui.click()
            pyautogui.PAUSE = .3
            time.sleep(1)

        else:
            print("no VR")
            sys.exit(0)

def write_notes(filename, last_ran,last_success, notes, marked):
    f = open(filename, "w")
    last_ran_string = "Last Ran: " + " ".join(last_ran)
    last_success_string = "Last Success: " + " ". join(last_success)
    fileout = last_ran_string = last_ran_string + "\n" + last_success_string + "\n" + notes + "\n" + marked
    f.write(fileout)
    f.close

def mark_payments():
    if len(sys.argv) > 3:
        customers = get_customers(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) == 3:
        customers = get_customers(sys.argv[1], int(sys.argv[2]), None)
    elif len(sys.argv) == 2:
        customers = get_customers(sys.argv[1], None, None)
    else:
        customers = [[]]
    notes = "Notes: \n"
    marked = "Marked: \n"
    last_ran = []
    last_success = []

    for customer in customers:
        check_open()
        pyautogui.PAUSE = .2
        lastname = pyautogui.locateOnScreen('img/lastnameinput.png', confidence=.9)
        if lastname == None:
            print("no last name")
            break
        pyautogui.moveTo(lastname)
        pyautogui.doubleClick()
        endindex = len(customer) - 1
        pyautogui.write(" ".join(customer[1:endindex]))
        firstname = pyautogui.locateOnScreen('img/firstnameinput.png', confidence=.9)
        if firstname == None:
            print('no first name')
            break
        pyautogui.moveTo(firstname)
        pyautogui.doubleClick()
        pyautogui.write(customer[0])
        pyautogui.press('enter')
        morethanone = pyautogui.locateOnScreen('img/morethanonencg.png', confidence=.9)
        print(morethanone)
        if morethanone:
            print('more than one with that name')
            notes += " ".join(customer) + " had more than one result" + "\n"
            pyautogui.press('esc')
            write_notes("log.txt", last_ran, last_success, notes, marked)
            check_open()
            continue
        pyautogui.press('enter')
        pyautogui.press('enter')
        time.sleep(1)
        subtotalimg = pyautogui.locateOnScreen('img/subtotal.png', confidence=.9)
        pyautogui.moveTo(subtotalimg)
        pyautogui.move(0, 23)
        pyautogui.doubleClick()
        pyautogui.doubleClick()
        #time.sleep(1)
        multilease = pyautogui.locateOnScreen('img/multiplelines.png')
        if multilease:
            print("multiple leases")
            pyautogui.press('esc')
            pyautogui.press('enter')
            notes += " ".join(customer) + " has multiple leases" + "\n"
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('enter')
            write_notes("log.txt", last_ran, last_success, notes, marked)
            continue
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('c')
        pyautogui.keyUp('c')
        pyautogui.keyUp('ctrl')
        subtotal = float(pyperclip.paste())
        print("subtotal: ", subtotal)
        amount_to_charge = float(customer[endindex])
        
        if subtotal == 0.0:
            print("already marked")
            pyautogui.press('esc')
            pyautogui.press('enter')
            notes += " ".join(customer) + " already marked" + "\n"
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('enter')
            last_ran = customer
            write_notes("log.txt", last_ran, last_success, notes, marked)
            continue

        if subtotal == False:
            print("could not copy subtotal")
            pyautogui.press('esc')
            pyautogui.press('enter')
            notes += " ".join(customer) + " couldn't copy subtotal" + "\n"
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('enter')
            last_ran = customer
            write_notes("log.txt", last_ran, last_success, notes, marked)
            continue

        elif amount_to_charge == subtotal:
            print("It Matches!")
            pyautogui.press('F10')
            payout = pyautogui.locateOnScreen('img/payout.png', confidence=.9)
            if payout:
                notes += " ".join(customer) + " Pays Off Today" + "\n"
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('enter')
                pyautogui.press('enter')
                last_ran = customer
                write_notes("log.txt", last_ran, last_success, notes, marked)
                continue
            print("no payout")
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('enter')
            pyautogui.press('enter')
            last_success = customer
            last_ran = customer
            marked += " ".join(customer) + " marked \n"
            write_notes("log.txt", last_ran, last_success, notes, marked)
            continue

        elif float(amount_to_charge) > float(subtotal) - .05 and float(amount_to_charge) < float(subtotal) + .05:
            print("close enough")
            pyautogui.write(str(amount_to_charge))
            pyautogui.press('F10')
            payout = pyautogui.locateOnScreen('img/payout.png', confidence=.9)
            if payout:
                notes += " ".join(customer) + " Pays Off Today" + "\n"
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('enter')
                pyautogui.press('enter')
                write_notes("log.txt", last_ran, last_success, notes, marked)
                continue
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('enter')
            last_success = customer
            last_ran = customer
            marked += " ".join(customer) + " marked off by "+ str(round(float(subtotal) - float(amount_to_charge), 2))  + "\n"
            write_notes("log.txt", last_ran, last_success, notes, marked)
            continue

        else:
            print("does not match")
            pyautogui.press('esc')
            pyautogui.press('enter')
            notes += " ".join(customer) + " amount didn't match" + "\n"
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('enter')
            last_ran = customer
            write_notes("log.txt", last_ran, last_success, notes, marked)
            continue
        
        

mark_payments()