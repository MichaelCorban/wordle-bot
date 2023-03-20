import pyautogui
import random
import webscraper

semantle_list_file = open("wordlist10000.txt", "r")

# append each line in txt file to list
semantle_word_list = []
for line in semantle_list_file:
  semantle_word_list.append(line)

semantle_list_file.close()

# remove newline characters from end of each element in list
semantle_word_list = list(map(lambda s: s.strip(), semantle_word_list))

# shuffle to randomize semantle word order
random.shuffle(semantle_word_list)

def semantle():
    # pause between keypresses for pyautogui measured in seconds
    pyautogui.PAUSE = 0.01
    # iterate through entire list and type out each individual character of each element
    for x in semantle_word_list:
        for y in range(len(x)):
            pyautogui.press(x[y])
        pyautogui.press('enter')


pyautogui.sleep(5)
semantle()



