from selenium.webdriver.edge.service import Service
#from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

incidents_href_dict = {}
ASSIGNED_TO_EMAIL = "chiranjib.bhattacharyya@pwc.com"
path = "C:/Users/cbhattacha015/OneDrive - PwC/Downloads/Selenium/Edgedriver/msedgedriver.exe" 
#path = "C:/Users/cbhattacha015/OneDrive - PwC/Downloads/Selenium/Chromedriver/chromedriver.exe" 

service = Service(executable_path=path)
options = webdriver.EdgeOptions()
#options = webdriver.ChromeOptions()
driver = webdriver.Edge(service=service, options=options)
#driver = webdriver.Chrome(service=service, options=options)
action = webdriver.ActionChains(driver)

url_normal      ="https://pwcnetwork.service-now.com/nav_to.do?uri=%2Ftask_list.do%3Fsysparm_query%3Dactive%253Dtrue%255Eassignment_groupDYNAMICd6435e965f510100a9ad2572f2b47744%255Estate!%253D6%255Eassigned_toISEMPTY%255Epriority%253D4%255Eurgency%253D4%255EORurgency%253D3%255Eshort_descriptionLIKEDocuSign%255EORshort_descriptionLIKELock%255EORshort_descriptionLIKERedirect%255EORshort_descriptionLIKEQualtrics%255EORshort_descriptionLIKEReport%255EnumberSTARTSWITHSCTASK%255Eassignment_groupNOT%2520LIKECHECKPOINT%255Eassignment_groupNOT%2520LIKEPwC%2520IT%2520-%2520APP%2520SPT%2520-%2520QUALTRICS%2520CL%2520SOLUTION%26s"
url_all         ="https://pwcnetwork.service-now.com/nav_to.do?uri=%2Ftask_list.do%3Fsysparm_query%3Dactive%253Dtrue%255Eassignment_groupDYNAMICd6435e965f510100a9ad2572f2b47744%255Estate!%253D6%255Eassigned_toISEMPTY%255Eassignment_groupNOT%2520LIKECHECKPOINT%255Eassignment_groupNOT%2520LIKEPwC%2520IT%2520-%2520APP%2520SPT%2520-%2520QUALTRICS%2520CL%2520SOLUTION%26sysparm_first_row%3D1%26sys"
driver.get(url_normal)

email = driver.find_element(By.ID, 'initEmail')
email.send_keys("a@pwc.com")
email.send_keys(Keys.RETURN)
WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(20)
element = driver.find_element(By.TAG_NAME, "body")
element = element.find_elements(By.TAG_NAME, "*")
macroponent_id = element[8].tag_name

def get_gsft_main_iframe(macroponent_id):
    time.sleep(0.05)
    iframe = driver.execute_script("""return document.querySelector("%s").shadowRoot.querySelector("sn-canvas-appshell-root").querySelector("sn-canvas-appshell-layout").querySelector("iframe")""" % macroponent_id)
    return iframe

cnt = 0
while True:
    if cnt == 40: break
    try:
        driver.switch_to.frame(get_gsft_main_iframe(macroponent_id))
        tbody = driver.find_element(By.XPATH, """//table[@id="task_table"]/tbody""")
        trs = tbody.find_elements(By.XPATH, './tr')
        if trs:                          
            action.context_click(trs[0]).perform()
            driver.find_element(By.XPATH, """//*[@id="context_list_rowtask"]/div[10]""").click()
            cnt += 1
        else:
            print(f"{cnt} Tickets...")
        driver.refresh()
    except Exception as ex:
        print(ex)

time.sleep(5)
driver.close()
driver.quit()
print("Exiting Program")
