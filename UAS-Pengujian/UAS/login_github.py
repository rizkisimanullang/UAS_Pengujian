from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, username, password):
    driver.get('https://github.com/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_field')))
    username_box = driver.find_element(By.ID, 'login_field')
    password_box = driver.find_element(By.ID, 'password')
    button_login = driver.find_element(By.NAME, 'commit')
    username_box.send_keys(username)
    password_box.send_keys(password)
    button_login.click()

#login benar
def login_success(driver):
    login(driver, "rizkisimanullang", "R1zk1aj4")
    WebDriverWait(driver, 10).until(EC.title_contains("GitHub"))
    assert "GitHub" in driver.title, "Login failed"

#login kedua masukan salah
def login_failure(driver):
    login(driver, "lainrizki", "inipassword")
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Incorrect username or password.')]"))
    )
    assert error_message is not None, "Error message not found for incorrect credentials"

#login tanpa masukan
def login_failure_empty(driver):
    login(driver, "", "")
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Username or email address')]"))
    )
    assert element is not None, "Error message not found for empty credentials"

if __name__ == '__main__':
    driver = webdriver.Chrome()
    try:
        login_success(driver)
        login_failure(driver)
        login_failure_empty(driver)
    finally:
        driver.quit()
