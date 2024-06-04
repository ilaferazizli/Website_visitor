import os
import time
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

check = {"SDF1", "SDF2", "TSI", "SSI"}
codes = ["CODE", "N", "M", "L", "SUBJ", "AKTS", "DAV", "SDF1", "SDF2", "TSI", "DVM", "SSI", "EI", "TI", "ORT"]

def createDatabase(marks_json_m):
    with open(database_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(marks_json_m, indent=4))

def checkGrades(marks_json_m):
    changed = []
    marks_json = {}
    try:
        with open(database_path, "r", encoding="utf-8") as file:
            marks_json = json.load(file)
    except (json.decoder.JSONDecodeError):
        createDatabase(marks_json_m)
        changed.append("Database it gününə qalıb!")
        return changed
    except FileNotFoundError:
        createDatabase(marks_json_m)
        changed.append("Yeni Database yaradıldı.")
        return changed
    except Exception as e:
        changed.append("Zortladım: {e}")
    key = list(marks_json_m.keys())[0]
    if not key in marks_json:
        changed.append("Yeni Semestr: " + key)
    else:
        for i, subj in enumerate(marks_json_m[key]):
            for ky, value in subj.items():
                if ky in check:
                    value2 = marks_json[key][i][ky]
                    if (value != value2):
                        changed.append(marks_json[key][i]["CODE"] + " - " + marks_json[key][i]["SUBJ"] + " - " + ky + " ||" + value + "||")

    marks_json[key] = marks_json_m[key]
    with open(database_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(marks_json, indent=4))
    return changed

def filterSoup(page_source):
    semestr = []
    soup = BeautifulSoup(page_source, "html.parser")

    for s in soup.find('select').findChildren('option')[1:]:
       semestr.append(s.text)

    i = 0
    res = {}
    subRes = {semestr[-1]: []}
    for s in soup.find('div', {"class": "table-responsive"}).find_all('tr')[1:-1]:
        subSubRes = {}
        subRes[semestr[-1]].append(subSubRes)
        for index, element in enumerate(s.findChildren('td')[:-1]):
            subSubSubRes = {codes[i]: element.text if index == 4 else
                                    element.text
                                    .replace("\n","")
                                    .replace(" ","")
                                    .replace("\t", "")
                                    .replace("\xa0","")}
            subRes[semestr[-1]][-1].update(subSubSubRes)
            i+=1
        i = 0
        res.update(subRes)
    return checkGrades(res)

username=os.getenv('BEU_USERNAME')
password=os.getenv('BEU_PASSWORD')
webhook_url=os.getenv('WEBHOOK_URL')
role_id=os.getenv('MENTION_ID')
log_path=os.getenv('LOG_PATH')
database_path=os.getenv("DATABASE_JSON")

if not username or not password or not webhook_url or not role_id or not log_path or not database_path:
    print('[ERROR] ENOUGH INPUTS WERE NOT GIVEN!')
    exit()

Options = webdriver.ChromeOptions()
Options.add_argument('--headless')
Options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=Options)
driver.get("https://my.beu.edu.az/index.php?mod=grades")
time.sleep(5)
driver.refresh()

username_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")

username_input.send_keys(username)
password_input.send_keys(password)

login_button = driver.find_element(By.NAME, "LogIn")
login_button.click()
time.sleep(5)

#Tms xəbərdarlıqlarını keç
try:
    alert_button = driver.find_element(By.XPATH, '//input[@class="btn btn-default" and @name="btnRead" and @value="Oxudum"]')
    if alert_button:
        alert_button.click()
except:
    pass

driver.get("https://my.beu.edu.az/index.php?mod=grades")

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

page_source = driver.page_source
driver.close()
driver.quit()
changed = filterSoup(page_source)

with open(log_path, "a", encoding="utf-8") as file:
    file.write(f"{datetime.now()} | Səhifəyə daxil olundu.\n")
    if not changed == []:
        embed = {
            "title": datetime.now().strftime("%H:%M:%S, %m/%d/%Y"),
            "description": "",
            "color": 3468224
        }
        msg = {
            "content": f"||<@&{role_id}>||",
            "embeds" : [embed]
        }
        for i in changed:
            file.write(f"{datetime.now()} | " + i + "\n")
            embed["description"] += i + "\n"
        result = requests.post(webhook_url, data=json.dumps(msg), headers={'Content-Type': 'application/json'})
        if 200 <= result.status_code < 300:
            file.write(f"{datetime.now()} | Webhooku basdım {result.status_code}\n")
        else:
            file.write(f"{datetime.now()} | Başaramadık abi... {result.status_code}\n")
    else:
        file.write(f"{datetime.now()} | Bıraktığım gibi.\n")