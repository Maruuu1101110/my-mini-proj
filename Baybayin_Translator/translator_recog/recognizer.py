import json
import os
import time

os.system("clear")

def load_file():
    with open("translator_recog/data_set.json","r") as lfile:
        return json.load(lfile)
data = load_file()

def slowPrint(words):
    print("Baybayin: ",end="",flush=True)
    for i in words:
        print(i,end="",flush=True)
        time.sleep(0.1)
    print()

def process(words):
    words = list(words)
    #print(words)
    new_words = []
    i = 0
    while i < len(words):
        matched = False
        if words[i] == " ":
            new_words.append(" ")
            i += 1
            continue

        if words[i] in '""<>/?:;[]{}|\!@#$%^&*()_-+=~``':
            new_words.append(words[i])
            i += 1
            continue

        if i + 2 < len(words):
            trio = words[i] + words[i + 1] + words[i+2]
            for value, keyword_list in data.items():
                if trio in keyword_list:
                    new_words.append(value)
                    i += 3
                    matched = True
                    break

        if not matched and i + 1 < len(words):
            pair = words[i] + words[i + 1]
            for value, keyword_list in data.items():
                if pair in keyword_list:
                    new_words.append(value)
                    i += 2
                    matched = True
                    break

        if not matched:
            for value, keyword_list in data.items():
                if words[i] in keyword_list:
                    new_words.append(value)
                    matched = True
                    break
                
            i += 1


    return "".join(new_words)

## Debug ##
def main(): 
    while True:
        user_input = input("Prompt: ").lower()
        if user_input == "q":
            break
        slowPrint(process(user_input))


if __name__=="__main__":
    main()
