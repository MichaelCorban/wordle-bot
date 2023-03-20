import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

current_row = 0

driver = None

def open_driver():
    global driver
    # open Wordle website on Chrome browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.nytimes.com/games/wordle/index.html")

def quit_driver():
    global driver, current_row
    driver.quit()
    driver = None
    current_row = 0

def click_x():
    button = driver.execute_script('''return document.querySelector('game-app').shadowRoot.querySelector('game-modal')
                            .shadowRoot.querySelector('game-icon').shadowRoot''')
    button.find_element(By.TAG_NAME, "svg").click()

# retrieve tile html
def get_tile(row, col):
    tiles = row.find_elements(By.TAG_NAME, "game-tile")
    return (tiles[col].get_attribute('outerHTML'))

# retrieve row html
def get_row(row_num):
    return driver.execute_script('''return document.querySelector("game-app").shadowRoot.querySelectorAll("game-row")[
                                    ''' + str(row_num) + '''].shadowRoot''')

# types the word letter by letter
def type_word(word):
    type = driver.find_element(By.TAG_NAME, "body")
    for x in range(len(word)):
        type.send_keys(word[x])
        time.sleep(1)
    type.send_keys(Keys.RETURN)

# returns true if game has been won
def win_cond():
    time.sleep(2)
    global current_row
    if current_row > 0:
        win_row = current_row - 1
    else:
        win_row = 0

    if win_row < 6:
        shadow = driver.execute_script('''return document.querySelector("game-app").shadowRoot''')
        tile = shadow.find_elements(By.TAG_NAME, "game-row")

        # space before win is important to prevent user entered words from interfering
        if " win" in tile[win_row].get_attribute('outerHTML'):
            return True
    elif win_row >= 6:
        return False
    return False

# retrieve letters that are inputted
def get_letters(row):
    letters = ""
    if row < 6:
        for x in range(5):
            letters += get_tile(get_row(row), x)[19]
    return letters

# retrieve evaluations for letters (green, yellow, gray)
def get_evaluations(row):
    evals = []
    if row < 6:
        for x in range(5):
            if "absent" in get_tile(get_row(row), x):
                evals.append(0)
            elif "present" in get_tile(get_row(row), x):
                evals.append(1)
            elif "correct" in get_tile(get_row(row), x):
                evals.append(2)
            else:
                evals.append(-1)
    return evals