import random
import webscraper
import date
import time
import text

inputted_words = []
inputted_evals = []
wordle_word_list = []


def word_list():
    global wordle_word_list, inputted_words, inputted_evals
    # resetting inputted_words and inputted_evals to clear previous Wordle game
    inputted_words = []
    inputted_evals = []
    #wordle_list_file = open("legalwordswordle.txt", "r")
    wordle_list_file = open("wordlesolutions.txt", "r")
    # append each line in txt file to list
    wordle_word_list = []
    for line in wordle_list_file:
      wordle_word_list.append(line)
    wordle_list_file.close()

    # remove newline characters from end of each element in list
    wordle_word_list = list(map(lambda s: s.strip(), wordle_word_list))

    # shuffle to randomize semantle word order
    random.shuffle(wordle_word_list)

def store_words(word, evals):
    global inputted_words, inputted_evals
    inputted_words.append(word)
    inputted_evals.append(evals)

# reduces the list of legal words down to possible words that work with the revealed logic (green, yellow, gray)
def reduce_list(word, evals):
    absent = ""
    present = ""
    correct = ""
    present_index = []
    correct_index = []

    for x in range(len(evals)):
        if evals[x] == 0:
            absent += word[x]
        elif evals[x] == 1:
            present += word[x]
            present_index.append(x)
        elif evals[x] == 2:
            correct += word[x]
            correct_index.append(x)

    for y in absent:
        if y in present:
            absent = absent.replace(y, "")
        if y in correct:
            absent = absent.replace(y, "")

    # reversed in order to prevent skipping words in list since removing while iterating can cause problems
    for z in reversed(wordle_word_list):
        breaker = False
        for a in absent:
            if a in z:
                wordle_word_list.remove(z)
                breaker = True
                break
        if breaker != True:
            for b in present_index:
                if z[b] == word[b]:
                    wordle_word_list.remove(z)
                    breaker = True
                    break
        if breaker != True:
            for c in present:
                if c not in z:
                    wordle_word_list.remove(z)
                    breaker = True
                    break
        if breaker != True:
            for d in correct_index:
                if z[d] != word[d]:
                    wordle_word_list.remove(z)
                    break

# mimic share function of Wordle
def share():
    num = str(date.wordle_number())
    message = "Wordle " + num + " "
    if webscraper.win_cond() == True:
        message += str(webscraper.current_row) + "/6\n\n"
    else:
        message += "X/6\n\n"

    #message += "done by WordleBot :)\n\n"

    for x in inputted_evals:
        for y in range(len(x)):
            if x[y] == 0:
                message += "⬜"
            elif x[y] == 1:
                message += "🟨"
            elif x[y] == 2:
                message += "🟩"
            else:
                return "-1"
        message += "\n"
    return message


# plays Wordle!
def wordle():
    webscraper.open_driver()
    webscraper.click_x()
    word_list()
    if (webscraper.win_cond() == False and webscraper.current_row < 6):
        print("Started")
        # chooses random word to start with, types it, removes it from the list, and increments the current row by one
        randint = random.randint(0, len(wordle_word_list) - 1)
        webscraper.type_word(wordle_word_list[randint])
        store_words(wordle_word_list[randint], webscraper.get_evaluations(webscraper.current_row))
        wordle_word_list.remove(wordle_word_list[randint])
        webscraper.current_row += 1

    # loop to continue guessing and reducing the possible words until the game is won or lost
    while (webscraper.win_cond() == False and webscraper.current_row < 6):
        reduce_list(webscraper.get_letters(webscraper.current_row - 1), webscraper.get_evaluations(webscraper.current_row - 1))
        randint = random.randint(0, len(wordle_word_list) - 1)
        webscraper.type_word(wordle_word_list[randint])
        store_words(wordle_word_list[randint], webscraper.get_evaluations(webscraper.current_row))
        wordle_word_list.remove(wordle_word_list[randint])
        webscraper.current_row += 1
    print("Finished")
    shared = share()
    webscraper.quit_driver()
    return shared

wordle()