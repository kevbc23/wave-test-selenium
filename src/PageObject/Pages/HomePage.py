#Elements Definition
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import driver

base_url = "https://web-stag.hispasatprod.opentv.com/"

class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.username = "input_username"
        self.password = "input_password"

    def get_username(self):
        return self.driver.find_element(By.ID, self.username)

    def get_password(self):
        return self.driver.find_element(By.ID, self.password)

    def login(self, username: str, password: str):

        # Input User
        user_input = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='input_username']")))
        user_input.clear()
        user_input.send_keys(username)

        # Input Password
        pass_input = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='input_password']")))
        pass_input.clear()
        pass_input.send_keys(password)

        # Click in login button
        login_btn = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-testid='button-signon-text']")))
        login_btn.click()

        print("✅ Login exitoso")

    def cerrar_sesion(self):

        # Encontramos el menu usuario
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="username-text"]')))
        menu_user = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='userAccountDropdown']")))
        menu_user.click()

        # Cerramos sesión
        btn_cerrar_sesion = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Cerrar sesión')]")))
        btn_cerrar_sesion.click()

        print("✅ Se cerró la sesión.")


