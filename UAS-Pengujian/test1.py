from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--windows-size=1920,1080")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(10)
from time import sleep

driver.get("https://www.python.org")

while (True):
    pass

