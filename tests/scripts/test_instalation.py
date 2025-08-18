import time

from pytest import mark
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import none_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import app_config

def login(driver: WebDriver, username, password):

    wait = WebDriverWait(driver, 10)

    #Input User
    user_input = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "[data-testid='input_username']")))
    user_input.clear()
    user_input.send_keys(username)

    #Input Password
    pass_input = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "[data-testid='input_password']")))
    pass_input.clear()
    pass_input.send_keys(password)

    # Click in login button
    login_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-testid='button-signon-text']")))
    login_btn.click()

    print("✅ Login exitoso")

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


def test_get_url_olvide_contrasena(app_config, driver: WebDriver):

    driver.get(app_config.base_url)
    wait = WebDriverWait(driver, 10)

    #Guardamos el ID de la ventana
    login_window = driver.current_window_handle

    btn_olvide_contrasena = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='recover-password-text']")))
    btn_olvide_contrasena.click()

    for window_handle in driver.window_handles:
        if window_handle != login_window:
            driver.switch_to.window(window_handle)
            break

    url_olvide_contrasena = driver.current_url

    assert url_olvide_contrasena is not None, "No se encontró la URL: Olvidé Contraseña"
    print("URL: Olvidé contraseña : ", url_olvide_contrasena)


def test_get_url_term_and_conditions(app_config, driver: WebDriver):

    driver.get(app_config.base_url)
    wait = WebDriverWait(driver, 5)

    #Guardamos el ID de la ventana
    login_window = driver.current_window_handle

    btn_term_and_cond = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='terms-condition-text']")))
    btn_term_and_cond.click()

    for window_handle in driver.window_handles:
        if window_handle != login_window:
            driver.switch_to.window(window_handle)
            break

    url_term_and_cond = driver.current_url

    assert url_term_and_cond is not None, "No se encontró la URL: Olvidé Contraseña"
    print("URL: Términos y Condiciones : ", url_term_and_cond)


def test_get_url_ayuda(app_config, driver: WebDriver): #Se obtiene desde el menú de usuario
    driver.get(app_config.base_url)
    wait = WebDriverWait(driver, 5)

    login(driver, "ajcordova@hispasat.pe", "123456")

    # Esperar que desaparezca animación de carga
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "[data-testid='Loading_Dotted']")))

    home_url = "https://web-stag.hispasatprod.opentv.com/discover"
    wait.until(EC.url_to_be(home_url))

    # Guardamos el ID de la ventana
    login_window = driver.current_window_handle

    menu_user = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='userAccountDropdown']")))
    nombre_usuario = menu_user.find_element(By.CSS_SELECTOR, "[data-testid='username-text']").text

    print(f"Usuario logueado: {nombre_usuario}")
    menu_user.click()

    #Clic en botón ayuda
    btn_ayuda = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Ayuda')]")))
    btn_ayuda.click()

    #Cambiar de ventana
    for window_handle in driver.window_handles:
        if window_handle != login_window:
            driver.switch_to.window(window_handle)
            break

    url_olvide_contrasena = driver.current_url

    assert url_olvide_contrasena is not None, "No se encontró la URL: Olvidé Contraseña"
    print("URL: Ayuda : ", url_olvide_contrasena)


def test_logo_de_marca (app_config,driver: WebDriver):
    driver.get(app_config.base_url)
    wait = WebDriverWait(driver, 10)

    logo_div = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[style*='icon_logo.webp']"))
    )
    #Extraer medidas del logo
    size = logo_div.size
    width = size['width']
    height = size['height']

    print(f"📐  Medidas del logo -> Ancho: {width}px, Alto: {height}px")

    #Validar medidas esperadas
    assert width == 155, f"❌ El ancho esperado era 155px pero se obtuvo {width}px"
    assert height == 97, f"❌ El alto esperado era 96px pero se obtuvo {height}px"

    print("✅ Validación correcta: las medidas del logo coinciden con lo esperado.")

@mark.ui
def test_fondo_bienvenida (app_config,driver: WebDriver):
    driver.get(app_config.base_url)
    wait = WebDriverWait(driver, 10)

    fondo_div = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[style*='splash_tv.webp']"))
    )

    assert fondo_div is not None, f"❌ No se muestra el fondo"

    print("✅ El fondo se muestra correctamente")







