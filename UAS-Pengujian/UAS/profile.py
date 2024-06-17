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

    # Check for two-factor authentication (2FA) page
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'otp')))
        print("Enter the authentication code:")
        otp_code = input()  # Prompt user to enter the 2FA code
        otp_box = driver.find_element(By.ID, 'otp')
        otp_box.send_keys(otp_code)
        verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify')]")
        verify_button.click()
    except:
        pass


def navigate_to_profile_edit(driver):
    driver.get('https://github.com/settings/profile')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Edit profile']"))
    )


def edit_name(driver, new_name):
    navigate_to_profile_edit(driver)
    name_field = driver.find_element(By.ID, 'user_profile_name')
    name_field.clear()
    name_field.send_keys(new_name)
    save_button = driver.find_element(By.XPATH, "//span[@class='Button-label'][normalize-space()='Save']")
    save_button.click()


def edit_bio(driver, new_bio):
    navigate_to_profile_edit(driver)
    bio_field = driver.find_element(By.ID, 'user_profile_bio')
    bio_field.clear()
    bio_field.send_keys(new_bio)
    save_button = driver.find_element(By.XPATH, "//span[@class='Button-label'][normalize-space()='Save']")
    save_button.click()


def test_edit_name(driver, new_name):
    edit_name(driver, new_name)
    # Assert name has been updated
    updated_name = driver.find_element(By.ID, 'user_profile_name').get_attribute('value')
    assert updated_name == new_name, "Name update failed"
    print(f"Test passed: Name updated to '{new_name}'.")


def test_edit_name_empty(driver):
    edit_name(driver, "")
    # Assert name cannot be empty (assuming GitHub throws an error or prevents saving)
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Name cannot be empty')]"))
    )
    assert error_message is not None, "Error message for empty name not found"
    print("Test passed: Empty name is not allowed.")


def test_edit_bio(driver, new_bio):
    edit_bio(driver, new_bio)
    # Assert bio has been updated
    updated_bio = driver.find_element(By.ID, 'user_profile_bio').get_attribute('value')
    assert updated_bio == new_bio, "Bio update failed"
    print(f"Test passed: Bio updated to '{new_bio}'.")


def test_edit_bio_empty(driver):
    edit_bio(driver, "")
    # Assert bio has been cleared
    updated_bio = driver.find_element(By.ID, 'user_profile_bio').get_attribute('value')
    assert updated_bio == "", "Bio clear failed"
    print("Test passed: Bio cleared successfully.")


if __name__ == '__main__':
    driver = webdriver.Chrome()  # Pastikan ChromeDriver ada di PATH
    try:
        login(driver, "rizkisimanullang", "R1zk1aj4")

        # Test edit name
        test_edit_name(driver, "rizki")

        # Test edit name to empty
        test_edit_name_empty(driver)

        # Test edit bio
        test_edit_bio(driver, "This is a new bio.")

        # Test edit bio to empty
        test_edit_bio_empty(driver)
    finally:
        driver.quit()
