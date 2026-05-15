import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

APP_URL = "http://172.17.0.1:5000"

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Remote(
        command_executor="http://selenium-hub:4444/wd/hub",
        options=chrome_options
    )
    yield driver
    driver.quit()

def test_page_title(driver):
    driver.get(APP_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Student Management System" in driver.find_element(By.TAG_NAME, "h1").text

def test_add_student_via_ui(driver):
    driver.get(APP_URL)
    wait = WebDriverWait(driver, 10)
    name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
    name_field.clear()
    name_field.send_keys("John Doe")
    grade_field = driver.find_element(By.ID, "grade")
    grade_field.clear()
    grade_field.send_keys("A")
    driver.find_element(By.ID, "addBtn").click()
    time.sleep(2)
    assert "John Doe" in driver.page_source
