"""
Автотесты формы логина на https://the-internet.herokuapp.com/login
с использованием Selenium и pytest.
"""

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


LOGIN_URL = "https://the-internet.herokuapp.com/login"


@pytest.fixture
def driver():
    """
    Фикстура создания браузера.

    Selenium Manager автоматически скачает нужный ChromeDriver.
    Опции --headless и др. нужны для запуска в CI без графической среды.
    """
    options = Options()
    options.add_argument("--headless")            # запуск без UI
    options.add_argument("--no-sandbox")          # требуется в CI
    options.add_argument("--disable-dev-shm-usage")  # обход ограничений /dev/shm

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def test_successful_login(driver):
    """Успешная авторизация с корректным логином и паролем."""
    driver.get(LOGIN_URL)

    # Заполняем форму
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

    # Нажимаем кнопку Login
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Проверяем сообщение об успехе
    flash = driver.find_element(By.ID, "flash").text
    assert "You logged into a secure area!" in flash

    # Дополнительно: URL должен измениться на /secure
    assert "/secure" in driver.current_url


def test_unsuccessful_login(driver):
    """Неудачная авторизация с неверными данными."""
    driver.get(LOGIN_URL)

    driver.find_element(By.ID, "username").send_keys("wronguser")
    driver.find_element(By.ID, "password").send_keys("wrongpassword")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Проверяем сообщение об ошибке
    flash = driver.find_element(By.ID, "flash").text
    assert "Your username is invalid!" in flash

    # Остались на странице логина
    assert "/login" in driver.current_url
