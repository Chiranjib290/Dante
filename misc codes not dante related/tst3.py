from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

path = "C:/Users/cbhattacha015/Downloads/Selenium/Edgedriver1/msedgedriver.exe"
service = Service(executable_path=path)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)
action = webdriver.ActionChains(driver)

# Replace with the actual URL
url = "https://survey.pwc.com/admin/reports/license-usage"
driver.get(url)

wait = WebDriverWait(driver, 10)

button_qualtrics = driver.find_element(By.XPATH, "//button[text()=\"Qualtrics sign in page\"]")

#button_sso.click()
button_qualtrics.click()

username = "chiranjib.bhattacharyya@pwc.com"
password = "Change@123456"

# Increase wait time to 20 seconds
wait = WebDriverWait(driver, 20)

try:
    # Wait for the username and password fields to be present and visible
    username_field = wait.until(EC.visibility_of_element_located((By.ID, 'UserName')))
    password_field = wait.until(EC.visibility_of_element_located((By.ID, 'UserPassword')))
    
    # Clear the fields and send the username and password
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    
    # Locate and click the login button
    login_button = driver.find_element(By.ID, 'loginButton')
    login_button.click()

    # Wait for the first dropdown to be visible and click it to display options
     # Click the first dropdown to display options
    first_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='license-dropdowns']//div[@class='option-menu-container'][1]//div[contains(@class, 'custom-select__value-container')]")))
    first_dropdown.click()
    
    # Add a short wait to ensure the dropdown options are displayed
    time.sleep(1)
    
    # Select 'Billable responses' from the first dropdown
    billable_responses_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Billable responses']")))
    billable_responses_option.click()
    
    # Click the second dropdown to display options
    second_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='license-dropdowns']//div[@class='option-menu-container'][2]//div[contains(@class, 'custom-select__value-container')]")))
    second_dropdown.click()
    
    # Add a short wait to ensure the dropdown options are displayed
    time.sleep(1)
    
    # Select 'Survey' from the second dropdown
    survey_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Survey']")))
    survey_option.click()

    date_range_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Date range')]")))
    date_range_dropdown.click()
    
    # Add a short wait to ensure the dropdown options are displayed
    time.sleep(1)
    
    # Wait for the 'Custom' option to be visible and select it
    custom_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Custom']")))
    custom_option.click()
   
    
    # Add a short wait to ensure the custom date inputs are displayed
    time.sleep(1)


    start_date_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='custom-day-range-input']//input[@class='datepicker-container'][1]")))
    start_date_input.send_keys(Keys.CONTROL + "a")
    start_date_input.send_keys(Keys.BACKSPACE)
    start_date_input.send_keys("Jan 1, 2025")
    start_date_input.send_keys(Keys.ENTER)



    print() 
except Exception as e:
    print(e)


print()