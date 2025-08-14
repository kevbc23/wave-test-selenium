#Elements Definition
from selenium.webdriver.common.by import By

base_url = "https://web-stag.hispasatprod.opentv.com/"

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.username = "input_username"
        self.password = "input_password"

    def get_username(self):
        return self.driver.find_element(By.ID, self.username)

    def get_password(self):
        return self.driver.find_element(By.ID, self.password)
