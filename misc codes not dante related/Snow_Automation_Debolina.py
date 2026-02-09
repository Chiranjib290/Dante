'''

    1. Install chromedriver from SCTASK17749261SCTASK17749261 based on your chrome version and OS
    2. Create a folder and keep the unziped chromdriver file in that folder eg: C:/Users/ankitas846/Documents/Selenium
    3. Install selenium https://pypi.org/project/selenium/ and save it in same folder (2)
    4. keep the script in the same folder (2)
    5. Set the variable ASSIGNED_TO_EMAIL with your email id
    6. Schedule a task using windows task scheduler

    Help:
        https://stackoverflow.com/questions/75613788/how-do-i-access-elements-in-the-shadow-dom-using-selenium-in-python
        https://cosmocode.io/how-to-interact-with-shadow-dom-in-selenium/#:~:text=To%20access%20the%20shadow%20DOM%20elements%20using%20JavaScript%20you%20first,shell')%3B%20var%20root%20%3D%20host.


'''

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


#import chromedriver_autoinstaller
#chromedriver_autoinstaller.install()

incidents_href_dict = {}
ASSIGNED_TO_EMAIL = "chiranjib.bhattacharyya@pwc.com"
path ="C:/Users/cbhattacha015/Downloads/Selenium/Chromedriver/chromedriver.exe" # give the path where you have kept you chrome driver file
url = "https://wwwpwcnetwork.pwc.myshn.net/nav_to.do?uri=%2Ftask_list.do%3Fsysparm_query%3Dactive%253Dtrue%255Eassignment_group%253Da8c97cb7dbf19344496a67a3ca961901%255EORassignment_group%253Db100b753db2f97001b209407db9619a7%255EORassignment_group%253D631ca3a71ba0f010e05a4152b24bcbca%255EORassignment_group%253D6391699b1b2f68149b0064e4604bcb8f%255EORassignment_group%253D17714449db252bcc8f3cf05c0c961928%255Estate!%253D6%255Eassigned_toISEMPTY%255Epriority%253D4%255Eurgency%253D4%255EORurgency%253D3%26sysparm_first_row%3D1%26sysparm_view%3D"
i=1

service = Service(executable_path= path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
action = webdriver.ActionChains(driver)
driver.get(url)
email = driver.find_element(By.ID, 'initEmail')
email.send_keys("a@pwc.com")
email.send_keys(Keys.RETURN)

## Wait for body html tag
WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

## Give some time to get things loaded
time.sleep(20)

## How to find macroponent-id tag name?
## first element inside <body></body> is always a macrocomponent element
element = driver.find_element(By.TAG_NAME, "body")
element = element.find_elements(By.TAG_NAME, "*")
macroponent_id= element[3].tag_name


def get_gsft_main_iframe(macroponent_id):
    time.sleep(0.5)
    iframe = driver.execute_script("""return document.querySelector("%s").shadowRoot.querySelector("sn-canvas-appshell-root").querySelector("sn-canvas-appshell-layout").querySelector("iframe")""" %macroponent_id)
    return iframe

cnt = 0
##driver.minimize_window()
while True:
    if cnt == 2 : break
    try:
        driver.switch_to.frame(get_gsft_main_iframe(macroponent_id))
        tbody = driver.find_element(By.XPATH, """//table[@id="task_table"]/tbody""")
        trs = tbody.find_elements(By.XPATH,'./tr')
        
        if not trs:
            print("Initiating refresh...")

        if trs:                          
            action.context_click(trs[0]).perform()
            driver.find_element(By.XPATH, """//*[@id="context_list_rowtask"]/div[10]""").click()
            time.sleep(1)
            print("\n\n\nTicket has been Picked Up.......................................................................................\n\n\n")
            cnt += 1
        driver.refresh()
    except Exception as ex:
        print("Something went wrong - %s" %ex)
                                                                  
time.sleep(2)
driver.close()
driver.quit()
print("Exiting Program")


