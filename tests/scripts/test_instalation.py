import time

from pytest import mark
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import none_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import app_config


def test_vers_actual_vers_principal(app_config, driver: WebDriver):

    driver.get(app_config.base_url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_username']"))).send_keys('ajcordova@hispasat.pe')
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_password']"))).send_keys('123456')
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='button-signon-text']"))).click()

    wait.until(EC.url_to_be("https://web-stag.hispasatprod.opentv.com/discover"))

    # wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "[data-testid='Loading_Dotted']")))

    home_url ="https://web-stag.hispasatprod.opentv.com/discover"
    if driver.current_url == home_url:
        #Encontrar el botón de configuración
        btn_settings = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[testid="settings-icon"]')))
        btn_settings.click()

    wait.until(EC.url_to_be("https://web-stag.hispasatprod.opentv.com/settings"))
    url_setting = "https://web-stag.hispasatprod.opentv.com/settings"

    if driver.current_url == url_setting :
        opcion_acerca_del_dispostivo = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Acerca del dispositivo')]")))
        opcion_acerca_del_dispostivo.click()

    version_actual = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='settingsAboutDeviceScreen_versionValue']"))).text
    version_principal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='settingsAboutDeviceScreen_coreVersionValue']"))).text

    print("Version Actual = ", version_actual)
    print("Version Principal = ", version_principal)

    assert version_actual is not None, "❌ El elemento no se encontró"
    assert version_principal is not None, "❌ El elemento no se encontró"



