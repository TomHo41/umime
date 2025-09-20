import random
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

location = r"C:\Users\honzi\AppData\Local\Google\Chrome\User Data\selenium-profile"
url = "https://www.umimecesky.cz/doplnovacka-podmet-holy-rozvity-nekolikanasobny-2"
start_time = time.time()
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY,
    text TEXT,
    answer TEXT
)
""")
#cursor.execute("DELETE FROM data WHERE text = 'Počasí se pokaz_.';")
conn.commit()
def add_sql(text, answer):
    cursor.execute("INSERT INTO data (text, answer) VALUES (?, ?)", (text, answer))
    conn.commit()
    print("Saved:", text, answer)
def click_button(button):
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "next"))
    )
    driver.find_element(By.XPATH, '//*[@id="next"]').click()
def no_answer():
    text = driver.find_element(By.XPATH, '//*[@id="question-content"]/span')
    orginal_text = str(text.text)
    op1 = driver.find_element(By.XPATH, '//*[@id="option0"]/span[@class="fmt-text"]')
    op2 = driver.find_element(By.XPATH, '//*[@id="option1"]/span[@class="fmt-text"]')
    button = driver.find_element(By.XPATH, '//*[@id="next"]')
    x = 0
    while x < 3:
        print("No answer saved")
        op1 = driver.find_element(By.XPATH, '//*[@id="option0"]/span[@class="fmt-text"]')
        op2 = driver.find_element(By.XPATH, '//*[@id="option1"]/span[@class="fmt-text"]')
        if x == 0:
            op1_text = str(op1.text)
            op2_text = str(op2.text)
        op1.click()
        time.sleep(3 + random.random() - random.random())     
        if orginal_text.split("_")[0] == driver.find_element(By.XPATH, '//*[@id="question-content"]/span').text[:len(orginal_text.split("_")[0])]:
            time.sleep(random.random() * 2 + 1)
            if "display: none" in driver.find_element(By.XPATH, '//*[@id="next"]').get_attribute("style"):
                print("no button")
                driver.find_element(By.XPATH, '//*[@id="option1"]/span[@class="fmt-text"]').click()
                add_sql(orginal_text, op2_text)
                time.sleep(random.random() * 2 + 1)
                if orginal_text.split("_")[0] == driver.find_element(By.XPATH, '//*[@id="question-content"]/span').text[:len(orginal_text.split("_")[0])]:
                    print("button w op2")
                    click_button(driver.find_element(By.XPATH, '//*[@id="next"]'))
                    break
                break
            else:
                print("button")
                time.sleep(random.random() * 3)
                click_button(button)
                add_sql(orginal_text, op1_text)
                break
        else:
            print("1")
            add_sql(orginal_text, op1_text)
            break
        x += 1
options = webdriver.ChromeOptions()
options.add_argument(rf"user-data-dir={location}")
# optional: options.add_argument(r"--profile-directory=Default")

# Remove “Chrome is being controlled” banner
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.get(url)
x = 0
time.sleep(2)
while x < 500:
    text = driver.find_element(By.XPATH, '//*[@id="question-content"]/span')
    element = driver.find_element(By.ID, "question-content")
    print(element.text)  # ✅ prints the full text inside the div
    orginal_text = str(text.text)
    op1 = driver.find_element(By.XPATH, '//*[@id="option0"]/span[@class="fmt-text"]')
    op2 = driver.find_element(By.XPATH, '//*[@id="option1"]/span[@class="fmt-text"]')
    button = driver.find_element(By.XPATH, '//*[@id="next"]')
    print(text.text, op1.text, op2.text)
    
    row = []
    cursor.execute(f"SELECT * FROM data WHERE text = '{orginal_text}';")
    row = cursor.fetchall()
    y = 0
    time.sleep(random.random() * 3 + 1)
    if driver.find_elements(By.CSS_SELECTOR, '[data-shield="3"]'):
        driver.find_element(By.CSS_SELECTOR, '[data-shield="3"]').click()
    if driver.find_elements(By.CSS_SELECTOR, '[data-shield="4"]'):
        print("Shield 4")
        break
        
    if len(row) != 0:
        print(row)
        answer = row[0][2]
        print(answer)
        while orginal_text.split("_")[0] == driver.find_element(By.XPATH, '//*[@id="question-content"]/span').text[:len(orginal_text.split("_")[0])]:
            if y >= 2:
                if answer == "í":
                    answer = "i"
                elif answer == "i":
                    answer = "í"
                elif answer == "ý":
                    answer = "y"
                elif answer == y:
                    answer = "ý"
                else:
                    y += 5
            if y >= 6:
                print("Deleted the answer")
                cursor.execute(f"DELETE FROM data WHERE id = '{row[0][0]}';")
                conn.commit
                no_answer()
            print("Answer found!", answer)
            if driver.find_element(By.XPATH, '//*[@id="option0"]/span[@class="fmt-text"]').text == answer:
                driver.find_element(By.XPATH, '//*[@id="option0"]/span[@class="fmt-text"]').click()
            elif driver.find_element(By.XPATH, '//*[@id="option1"]/span[@class="fmt-text"]').text == answer:
                driver.find_element(By.XPATH, '//*[@id="option1"]/span[@class="fmt-text"]').click()
            
            time.sleep(random.random() * 2)
            if not "display: none" in driver.find_element(By.XPATH, '//*[@id="next"]').get_attribute("style"):
                print("button!")
                click_button(driver.find_element(By.XPATH, '//*[@id="next"]'))
            y += 1 
            time.sleep(1)
        
    else:
        no_answer()
    time.sleep(random.random() * 2 + 3)
    x+=1






input("Press Enter when you want to close the browser...")  # <- pause here
driver.quit()
