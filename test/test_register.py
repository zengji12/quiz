from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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

def test_register_valid(driver):
    driver.get('http://127.0.0.1:8000/register.php')

    name = driver.find_element(By.NAME, 'name')
    email = driver.find_element(By.NAME, 'email')
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    repassword = driver.find_element(By.NAME, 'repassword')
    submit_button = driver.find_element(By.NAME, 'submit')

    name.send_keys('User')
    email.send_keys('user@mail.com')
    username.send_keys('user')
    password.send_keys('password')
    repassword.send_keys('password')
    submit_button.click()

    time.sleep(2)

    assert "index.php" in driver.current_url
    print("Register Valid Test Passed")

def test_register_username_exists(driver):
    driver.get('http://127.0.0.1:8000/register.php')

    name = driver.find_element(By.NAME, 'name')
    email = driver.find_element(By.NAME, 'email')
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    repassword = driver.find_element(By.NAME, 'repassword')
    submit_button = driver.find_element(By.NAME, 'submit')

    name.send_keys('User')
    email.send_keys('user@mail.com')
    username.send_keys('user')
    password.send_keys('password')
    repassword.send_keys('password')
    submit_button.click()

    time.sleep(2)

    error_message = driver.find_element(By.CSS_SELECTOR, '.alert.alert-danger').text
    assert 'Username sudah terdaftar !!' in error_message
    print("Register Username Exists Test Passed")

def test_register_password_mismatch(driver):
    driver.get('http://127.0.0.1:8000/register.php')

    name = driver.find_element(By.NAME, 'name')
    email = driver.find_element(By.NAME, 'email')
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    repassword = driver.find_element(By.NAME, 'repassword')
    submit_button = driver.find_element(By.NAME, 'submit')

    name.send_keys('User')
    email.send_keys('user@mail.com')
    username.send_keys('user2')
    password.send_keys('password')
    repassword.send_keys('wrongpassword')
    submit_button.click()

    time.sleep(2)

    error_message = driver.find_element(By.CLASS_NAME, 'text-danger').text
    assert 'Password tidak sama !!' in error_message
    print("Register Password Mismatch Test Passed")

def test_register_empty_fields(driver):
    driver.get('http://127.0.0.1:8000/register.php')

    submit_button = driver.find_element(By.NAME, 'submit')

    submit_button.click()

    time.sleep(2)

    error_message = driver.find_element(By.CSS_SELECTOR, '.alert.alert-danger').text
    assert 'Data tidak boleh kosong !!' in error_message
    print("Register Empty Fields Test Passed")

def run_tests():
    driver = init_driver()
    
    try:
        test_register_valid(driver)
        test_register_empty_fields(driver)
        test_register_username_exists(driver)
        test_register_password_mismatch(driver)
    finally:
        driver.quit()

run_tests()
