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
driver = webdriver.Chrome()  # Make sure ChromeDriver is in your PATH

def find_repository(driver, repo_name):
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    search_box.clear()
    search_box.send_keys(repo_name)
    search_box.submit()

    # Wait for search results to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'repo-list')]"))
    )
    repo_link = driver.find_element(By.XPATH, f"//input[@id='your-repos-filter']")
    return repo_link

def test_find_repository(driver, repo_name):
    repo_link = find_repository(driver, repo_name)
    assert repo_link is not None, f"Repository '{repo_name}' not found"
    print(f"Test passed: Repository '{repo_name}' found.")


def open_repository(driver, repo_name):
    repo_link = find_repository(driver, repo_name)
    repo_link.submit()  # submit the search query instead of clicking on the link

    # Wait for the repository page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[@class='js-repo-description']"))
    )
    print(f"Repository '{repo_name}' opened successfully.")


def test_open_repository(driver, repo_name):
    open_repository(driver, repo_name)
    assert driver.current_url.endswith(repo_name), f"Failed to open repository '{repo_name}'"
    print(f"Test passed: Opened repository '{repo_name}'.")


def create_repository(driver, repo_name, description=""):
    driver.get('https://github.com/new')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ':rg:')))

    repo_name_field = driver.find_element(By.ID, ':rg:')
    repo_desc_field = driver.find_element(By.ID, ':rh:')

    repo_name_field.clear()
    repo_desc_field.clear()

    repo_name_field.send_keys(repo_name)
    repo_desc_field.send_keys(description)

    create_repo_button = driver.find_element(By.XPATH, "//span[contains(text(),'Create repository')]")
    create_repo_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//strong[contains(text(), '{repo_name}')]"))
    )
    print(f"Repository '{repo_name}' created successfully.")


def test_create_repository(driver, repo_name, description=""):
    create_repository(driver, repo_name, description)
    assert driver.current_url.endswith(repo_name), f"Failed to create repository '{repo_name}'"
    print(f"Test passed: Created repository '{repo_name}' with description '{description}'.")


# Example usage
if __name__ == '__main__':
    driver = webdriver.Chrome()  # Pastikan ChromeDriver ada di PATH Anda
    try:
        login(driver, "rizkisimanullang", "R1zk1aj4")

        # Test find repository
        #test_find_repository(driver, "rizkisimanullang/GEMASTIK2023")

        # Test open repository
        test_open_repository(driver, "rizkisimanullang/GEMASTIK2023")

        # Test create repository
        #test_create_repository(driver, "UAS_PPKPL", "UAS Repositori")
    finally:
        driver.quit()
