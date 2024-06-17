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

# Initialize WebDriver
driver = webdriver.Chrome()

def install_order_with_data(driver, app_name, user_data):
    driver.get('https://github.com/marketplace')
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    search_box.clear()
    search_box.send_keys(app_name)
    search_box.submit()

    # Wait for search results and click on the app
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/marketplace/{app_name}')]"))
    ).click()

    # Wait for the app page to load and click install/buy button
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Install')]"))
    ).click()

    # buat isian data
    for field, value in user_data.items():
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, field))
        )
        input_element.clear()
        input_element.send_keys(value)

    # Submit the form to complete the order
    submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Complete order')]")
    submit_button.click()

    # Verify that the order was successful
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Thank you')]"))
    )
    print("Order completed successfully.")

def test_install_order_with_data(driver):
    app_name = "LambdaTest"  # isi nama app
    user_data = {
        "firstname": "rizki",
        "lastname": "simanullang",
        "Address (P.O. box, company name, c/o)": "jalan.123",
        "City ": "Banjarmasin",
        "usernameCountry/Region": "Indonesia",

    }
    install_order_with_data(driver, app_name, user_data)
    print("Test passed: Install order with data completed successfully.")

def install_order_without_data(driver, app_name):
    driver.get('https://github.com/marketplace')
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    search_box.clear()
    search_box.send_keys(app_name)
    search_box.submit()

    # tunggu pencarian
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/marketplace/{app_name}')]"))
    ).click()

    # tunggu load buat klik save
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Install')]"))
    ).click()

    # buat kirim data tanpa input
    submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Complete order')]")
    submit_button.click()

    # Verify that error messages appear
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'error')]"))
    )
    assert error_message is not None, "Error message not found for empty data submission"
    print("Error message displayed correctly for empty data submission.")

def test_install_order_without_data(driver):
    app_name = "LambdaTesst"  # isi dengan nama app
    install_order_without_data(driver, app_name)
    print("Test passed: Error message displayed for empty data submission.")


if __name__ == '__main__':
    driver = webdriver.Chrome()  # Pastikan ChromeDriver ada di PATH Anda
    try:
        login(driver, "rizkisimanullang", "R1zk1aj4")

        # Test install order with data
        test_install_order_with_data(driver)

        # Test install order without data
        test_install_order_without_data(driver)
    finally:
        driver.quit()
