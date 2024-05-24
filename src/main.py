from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import csv

# account and password

ACCOUNT = "ACCOUNT_HERE"
PASSWORD = "PASSWORD_HERE"

# class

schedule = []

for i in range(7):
    schedule.append([0, 0, 0, 0, 0])
print(schedule)

chinese_to_num = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 4
}

# url

LOGIN_SITE = "https://shcloud14.k12ea.gov.tw/HLHSHLC/Auth/Auth/CloudLogin"
STATIC_SITE = "https://shcloud14.k12ea.gov.tw/HLHSHLC/ICampus/StudentInfo/Index?page=%E7%BC%BA%E6%9B%A0%E7%B5%B1%E8%A8%88"

browser = webdriver.Chrome()

# login
browser.get(LOGIN_SITE)

identity_selections = browser.find_elements(By.XPATH, "//input[@name='loginType']")
# first one is student
btn = identity_selections[0].find_element(By.XPATH, "./..")
btn.click()

login_id = browser.find_element(By.XPATH, "//input[@name='LoginId']")
login_id.send_keys(ACCOUNT)

login_password = browser.find_element(By.XPATH, "//input[@name='PassString']")
login_password.send_keys(PASSWORD)

login_btn = browser.find_element(By.XPATH, "//button[@data-bind='click:btnDoLogin']")
login_btn.click()

sleep(1)

browser.get(STATIC_SITE)

sleep(3)

tab_detail = browser.find_element(By.XPATH, "//div[@id='tab_Details']")
tab_detail.click()

sleep(1)

table_hover = browser.find_element(By.XPATH, "//tbody[@class='table-hover']")

# iterate through children

tr_children = table_hover.find_elements(By.XPATH, ".//*")

print("Found " + str(len(tr_children)) + " entries")

for i in range(len(tr_children)):
    tr = tr_children[i]
    td_children = tr.find_elements(By.XPATH, ".//*")
    if len(td_children) < 2:
        continue
    date_text = td_children[0].text
    if date_text.strip() == "":
        continue

    print(date_text)
    weekday = chinese_to_num[date_text[11]]
    print(weekday)
    sum_text = td_children[1].text

    # 0,1,2,3: 4,5,6,7
    # 4,5,6,7: 9,10,11,12

    for j in range(4):
        text = td_children[j + 4].text.strip()
        if text == "事" or text == "曠":
            schedule[j][weekday - 1] += 1

    for j in range(4, 7):
        text = td_children[j + 5].text.strip()
        if text == "事" or text == "曠":
            schedule[j][weekday - 1] += 1
    
    print("")

for i in range(7):
    print("節 ", i, end = "\t")
    for j in range(5):
        print(schedule[i][j], end = "\t")
    print("")

with open('缺曠.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['"Session"', '"Monday"', '"Tuesday"', '"Wednesday"', '"Thursday"', '"Friday"'])
    for i in range(7):
        writer.writerow([i + 1] + schedule[i])

sleep(600)