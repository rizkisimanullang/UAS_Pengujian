from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login(driver, username, password):
    driver.get('https://github.com/')
    sign_in_button = driver.find_element(By.XPATH, "//a[@class='HeaderMenu-link HeaderMenu-link--sign-in flex-shrink-0 no-underline d-block d-lg-inline-block border border-lg-0 rounded rounded-lg-0 p-2 p-lg-0']")
    sign_in_button.click()
    time.sleep(2)  # tunggu untuk sign-in

    email_box = driver.find_element(By.ID, 'login')
    email_box.send_keys(username)
    next_button = driver.find_element(By.XPATH, "//input[@id='login_field']")
    next_button.click()
    time.sleep(2)  # tunggu untuk load pass

    password_box = driver.find_element(By.NAME, 'password')
    password_box.send_keys(password)
    next_button = driver.find_element(By.XPATH, "//input[@id='password']")
    next_button.click()
    time.sleep(2)  # tunggu proses selesai

def login_success(driver):
    login(driver, "rizkisimanullang", "R1zk1aj4")
    time.sleep(5)  # tunggu login berhasil
    profile_icon = driver.find_elements(By.XPATH, "//img[@id='img' and @alt='Avatar image']")
    assert len(profile_icon) > 0, "Login failed, profile icon not found."

def login_failure(driver):
    login(driver, "vivre.rizki@gmail.com", "bukanpassword")
    time.sleep(5)  # pesan error muncul,tunggu
    error_message = driver.find_elements(By.XPATH, "//input[@name='Passwd']")
    assert len(error_message) > 0, "Error message not found."

def login_failure_empty(driver):
    login(driver, "", "")
    time.sleep(5)  # pesan error muncul,tunggu
    error_message = driver.find_elements(By.XPATH, "//*[contains(text(),'Enter an email or phone number')]")
    assert len(error_message) > 0, "Error message not found."

if __name__ == '__main__':
    driver = webdriver.Chrome()
    try:
        login_success(driver)
        login_failure(driver)
        login_failure_empty(driver)
    finally:
        driver.quit()
