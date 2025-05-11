import os
import json
import shutil
import time
from translator_recog.recognizer import process,slowPrint

terminal_center = shutil.get_terminal_size().columns

def print_UI():
    os.system("cls" if os.name == "nt" else "clear")
    print("\n")
    print("==| BAYBAYIN - LATIN TRANSLATOR |==".center(terminal_center))
    print("\n")
    opt = ["Translate","Exit"]

    for num, item in enumerate(opt, start=1):
        print(f"[{num}] | {item}")
    
    user_inpt = input("|>> ").lower()
    if user_inpt == "1":
        return "Translator"
    elif user_inpt == "2":
        return "Exit"
    else:
        return "Unknown"

def translator():
    os.system("cls" if os.name == "nt" else "clear")
    print("\n")
    print("==| BAYBAYIN - LATIN TRANSLATOR |==".center(terminal_center))
    print("\n")
    while True:
        user = input("\n\nBaybayin: ").lower()
        slowPrint(process(user))
        if user == "q":
            break
            return

def main_process():
    while run:
        get_response = print_UI()
        
        if get_response == "Translator":
            translator()
        elif get_response == "Exit":
            break

if __name__=="__main__":
    run = True
    main_process()
