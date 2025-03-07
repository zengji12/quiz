import os
import logging
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

# Install ChromeDriver yang sesuai dengan versi Google Chrome
chromedriver_autoinstaller.install()

# Konfigurasi Logging
LOG_DIR = "test-results"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "test_log.txt"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def wait_for_server(url, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Server is up and running!")
                return True
        except requests.exceptions.ConnectionError:
            print("⏳ Waiting for server to start...")
        time.sleep(5)
    raise RuntimeError("❌ Server failed to start!")

BASE_URL = "http://127.0.0.1:8000/"
wait_for_server(BASE_URL)

def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def log_result(test_name, status, message=""):
    result = f"{test_name}: {status} - {message}"
    print(result)
    logging.info(result)

def run_test(driver, test_function):
    try:
        test_function(driver)
        log_result(test_function.__name__, "✅ PASSED")
    except AssertionError as e:
        log_result(test_function.__name__, "❌ FAILED", str(e))
    except Exception as e:
        log_result(test_function.__name__, "⚠️ ERROR", str(e))

def test_register_valid(driver):
    driver.get(BASE_URL + "register.php")
    driver.find_element(By.NAME, "name").send_keys("User")
    driver.find_element(By.NAME, "email").send_keys("user@mail.com")
    driver.find_element(By.NAME, "username").send_keys("user")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "repassword").send_keys("password")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "index.php" in driver.current_url

def test_register_username_exists(driver):
    driver.get(BASE_URL + "register.php")
    driver.find_element(By.NAME, "username").send_keys("user")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger").text
    assert "Username sudah terdaftar !!" in error_message

def test_register_password_mismatch(driver):
    driver.get(BASE_URL + "register.php")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "repassword").send_keys("wrongpassword")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "text-danger").text
    assert "Password tidak sama !!" in error_message

def test_register_empty_fields(driver):
    driver.get(BASE_URL + "register.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger").text
    assert "Data tidak boleh kosong !!" in error_message

def test_login_valid(driver):
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.NAME, "username").send_keys("reza")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "index.php" in driver.current_url

def test_login_empty_fields(driver):
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger").text
    assert "Data tidak boleh kosong !!" in error_message

def test_login_invalid_username(driver):
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.NAME, "username").send_keys("invalid_username")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger").text
    assert "Register User Gagal !!" in error_message

def test_login_invalid_password(driver):
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.NAME, "username").send_keys("reza")
    driver.find_element(By.NAME, "password").send_keys("wrong_password")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "login.php" in driver.current_url

def run_tests():
    driver = init_driver()
    try:
        test_cases = [
            test_register_valid,
            test_register_username_exists,
            test_register_password_mismatch,
            test_register_empty_fields,
            test_login_valid,
            test_login_empty_fields,
            test_login_invalid_username,
            test_login_invalid_password
        ]
        for test in test_cases:
            run_test(driver, test)
    finally:
        driver.quit()

run_tests()
