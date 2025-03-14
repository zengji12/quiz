from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Mode headless (tanpa UI)
    chrome_options.add_argument("--no-sandbox")  # Dibutuhkan agar berjalan di GitHub Actions
    chrome_options.add_argument("--disable-dev-shm-usage")  # Mencegah masalah shared memory di Linux
    chrome_options.add_argument("--disable-gpu")  # Tidak perlu GPU di server CI/CD
    
    # Set up WebDriver dengan konfigurasi yang sudah diperbaiki
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()  # Optional: max window for tests (in headless mode this will be default size)
    return driver

def test_login_valid(driver):
    driver.get('http://127.0.0.1:8000/login.php')
    driver.find_element(By.NAME, "username").send_keys("reza")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "submit").click()
    
    time.sleep(2)
    assert "index.php" in driver.current_url
    print("Login Valid Test Passed")

def test_login_empty_fields(driver):
    driver.get('http://127.0.0.1:8000/login.php')
    submit_button = driver.find_element(By.NAME, 'submit')
    submit_button.click()

    time.sleep(2)
    error_message = driver.find_element(By.CSS_SELECTOR, '.alert.alert-danger').text
    assert 'Data tidak boleh kosong !!' in error_message
    print("Login Without Data Test Passed")

def test_login_invalid_username(driver):
    driver.get('http://127.0.0.1:8000/login.php')
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.NAME, 'submit')

    username.send_keys('invalid_username')
    password.send_keys('password')
    submit_button.click()

    time.sleep(2)
    error_message = driver.find_element(By.CSS_SELECTOR, '.alert.alert-danger').text
    assert 'Register User Gagal !!' in error_message
    print("Login Invalid Username Test Passed")

def test_login_invalid_password(driver):
    driver.get('http://127.0.0.1:8000/login.php')
    
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.NAME, 'submit')

    username.send_keys('reza')
    password.send_keys('wrong_password')
    submit_button.click()

    time.sleep(2)

    assert "login.php" in driver.current_url
    print("Login Invalid Password Test Passed")

def run_tests():
    driver = init_driver()
    
    try:
        test_login_valid(driver)
        test_login_empty_fields(driver)
        test_login_invalid_username(driver)
        test_login_invalid_password(driver)
    finally:
        driver.quit()

run_tests()
