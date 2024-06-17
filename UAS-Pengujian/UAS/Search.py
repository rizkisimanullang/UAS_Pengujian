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
    driver.get('https://github.com/')
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    # Pastikan kotak pencarian bisa diinteraksi
    search_box.clear()
    search_box.send_keys(query)
    search_box.submit()

    # Tunggu sampai hasil pencarian ditampilkan
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'repo-list')]"))
    )
    return results

def positive_search_test(driver):
    query = "Selenium"
    results = search_github(driver, query)

    # Untuk memastikan hasil muncul
    assert len(driver.find_elements(By.XPATH, "//div[@class='overflow-hidden']")) > 0, "No search results found"
    print(f"Positive test passed: Search for '{query}' yielded results.")

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
        positive_search_test(driver)

        # Negative search test
        negative_search_test(driver)
    finally:
        driver.quit()
