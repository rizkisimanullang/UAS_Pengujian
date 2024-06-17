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

    #Tunggu auntentikasi
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'otp')))
        print("Enter the authentication code:")
        otp_code = input()  # buat memasukan kode
        otp_box = driver.find_element(By.ID, 'otp')
        otp_box.send_keys(otp_code)
        verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify')]")
        verify_button.click()
    except:
        pass

def search_github(driver, query):
    driver.get('https://github.com/dashboard')
    wait = WebDriverWait(driver, 30)
    search_box = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="query-builder-test"]'))
    )
    search_box.clear()
    search_box.send_keys(query)
    search_box.submit()

    # Wait for the search results to load
    wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="repository-list"]/ul/li'))
    )

def positive_search_test(driver):
    query = "SeleniumHQ"
    search_github(driver, query)

    # Add a delay to ensure the page has fully loaded
    import time
    time.sleep(2)

    # Verify that the search results are correct
    results = driver.find_elements(By.XPATH, "//div[@class='repository-list']/ul/li")
    assert len(results) > 0, "No search results found"
    for result in results:
        assert result.find_element(By.TAG_NAME, "h3").text.startswith(query), "Search result does not contain query"

def negative_search_test(driver):
    query = "MasakanPadangSayo"  # masukan hasil yang tidak ada/ tidak akan muncul
    search_github(driver, query)

    # Untuk menegaskan hasil tidak muncul
    no_results_text = "We couldn’t find any repositories matching"
    assert no_results_text in driver.page_source, "Search results found for unlikely query"
    print(f"Negative test passed: Search for '{query}' yielded no results.")

if __name__ == '__main__':
    driver = webdriver.Chrome()  # Make sure ChromeDriver is in your PATH
    try:
        # Login to GitHub (optional, required if you want to test as a logged-in user)
        login(driver, "rizkisimanullang", "R1zk1aj4")

        # Positive search test
        #positive_search_test(driver)

        # Negative search test
        negative_search_test(driver)
    finally:
        driver.quit()
