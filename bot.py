from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# CHROME_URL = r'E:\chromedriver-win64\chromedriver.exe'

driver = Chrome(options=options)
actions = ActionChains(driver)


def get_cae_marks(reg_no, pwd):
    print(reg_no, pwd)
    URL = 'https://erp.sathyabama.ac.in/account/login?returnUrl=%2F'
    driver.get(URL)

    dropdown = driver.find_element(By.XPATH,
                                   "/html/body/app-minton/app-login/div/div/div/div/div[1]/div/div[2]/select/option[3]")
    dropdown.click()

    register_input = driver.find_element(By.XPATH,
                                         "/html/body/app-minton/app-login/div/div/div/div/div[1]/div/div[3]/form/div[1]/input")
    register_input.send_keys(reg_no)

    password_input = driver.find_element(By.XPATH,
                                         "/html/body/app-minton/app-login/div/div/div/div/div[1]/div/div[3]/form/div[2]/input")
    password_input.send_keys(pwd)

    time.sleep(2)

    login_button = driver.find_element(By.XPATH,
                                       "/html/body/app-minton/app-login/div/div/div/div/div[1]/div/div[3]/form/div[3]/button")
    login_button.click()
    print(login_button.text)

    time.sleep(5)

    cae_button = driver.find_element(By.XPATH,
                                     "/html/body/app-minton/app-layout/div/app-view-student/div/div/div/div/div/div/div/div[2]/div/div/ngb-accordion/div/div[2]/div/div/a[9]")
    cae_button.click()

    time.sleep(8)

    lists = driver.find_elements(By.XPATH,
                                 "/html/body/app-minton/app-layout/div/app-view-student/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[3]/div/div/div[2]/div")
    print("End")

    sems = []
    tims = []

    cae1 = []
    cae2 = []
    # 1, 9
    for i in range(1, 9):
        try:
            titles = []
            marks = []
            out_of = []
            caes = []
            total_cae1 = 0
            total_cae2 = 0
            out_of_cae1 = 0
            out_of_cae2 = 0
            documents_cae1 = {}
            documents_cae2 = {}

            tabs = driver.find_element(By.XPATH,
                                       f"/html/body/app-minton/app-layout/div/app-view-student/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[3]/div/div/div[2]/div/ngb-accordion/div[{i}]/div/button/div")
            tabs.click()
            sems.append(tabs.text)
            time.sleep(3)

            results = driver.find_element(By.XPATH,  # here
                                          f"/html/body/app-minton/app-layout/div/app-view-student/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[3]/div/div/div[2]/div/ngb-accordion/div[{i}]/div[2]/div/div/table/tbody")
            for i in range(0, len(results.text.splitlines())):
                print("".join(results.text.splitlines()[i].split(" ")[-2]))
                titles.append(" ".join(results.text.splitlines()[i].split(" ")[2:-4]))
                marks.append(round(float("".join(results.text.splitlines()[i].split(" ")[-2]))))
                out_of.append(int("".join(results.text.splitlines()[i].split(" ")[-3])))
                caes.append(int("".join(results.text.splitlines()[i].split(" ")[-4])))

            # CAE-1 Marks
            for i in range(0, caes.count(1)):
                documents_cae1[titles[i]] = f"{marks[i]} / {out_of[i]}"
                total_cae1 += marks[i]
                out_of_cae1 += out_of[i]
            documents_cae1["Total Marks"] = f"{total_cae1} / {out_of_cae1}"
            # CAE-2 Marks
            for i in range(caes.count(1), caes.count(1) + caes.count(2)):
                documents_cae2[titles[i]] = f"{marks[i]} / {out_of[i]}"
                total_cae2 += marks[i]
                out_of_cae2 += out_of[i]
            documents_cae2["Total Marks"] = f"{total_cae2} / {out_of_cae2}"
            cae1.append(documents_cae1)
            cae2.append(documents_cae2)

        except NoSuchElementException:
            print("Skipping Unavailable Tabs")

        except ElementClickInterceptedException:
            print("Empty div")

    semesters_cae1 = {}
    semesters_cae2 = {}

    total_sems = {}

    for i in range(0, len(cae1)):
        semesters_cae1[f"Semester {len(sems) - i - 1}"] = cae1[i]

    for i in range(0, len(cae2)):
        semesters_cae2[f"Semester {len(sems) - i - 1}"] = cae2[i]

    for i in range(0, len(cae1)):
        total_sems[f"Semester {len(sems) - i - 1}"] = {
            "CAE-1": cae1[i],
            "CAE-2": cae2[i]
        }
    return total_sems
