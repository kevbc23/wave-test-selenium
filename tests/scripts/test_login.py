import time

from pytest import mark
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import none_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import app_config


def test_recuperar_contrasena(app_config, driver: WebDriver):
    driver.get(app_config.base_url)

    time.sleep(3)

    #Save ID of login window
    login_window = driver.current_window_handle
    print(login_window)

    driver.find_element(By.CSS_SELECTOR, "[data-testid='recover-password-text'").click()
    time.sleep(5)

    for window_handle in driver.window_handles:
        if window_handle != login_window:
            driver.switch_to.window(window_handle)
            break

    current_url = driver.current_url
    expected_url = 'https://extranet.telconet.ec/reiniciarContrasenia/changePasswordNetlifePlay'

    assert current_url == expected_url, f"❌ URL incorrecta: se esperaba '{expected_url}' pero se obtuvo '{current_url}'"

    print("✅ Flujo de recuperación de contraseña exitoso.")


def test_terminos_y_condiciones(app_config, driver: WebDriver):
    driver.get(app_config.base_url)

    time.sleep(3)

    # Save ID of login window
    login_window = driver.current_window_handle
    print(login_window)

    driver.find_element(By.CSS_SELECTOR, "[data-testid='terms-condition-text'").click()
    time.sleep(5)

    for window_handle in driver.window_handles:
        if window_handle != login_window:
            driver.switch_to.window(window_handle)
            break

    current_url = driver.current_url
    expected_url = 'https://www.netlife.ec/netlife-play-tyc/'

    assert current_url == expected_url, f"❌ URL incorrecta: se esperaba '{expected_url}' pero se obtuvo '{current_url}'"

    print("✅ URL de Términos y Condiciones validada correctamente.")


def test_login_with_credentials(app_config, driver: WebDriver):
    driver.get(app_config.base_url)

    time.sleep(5)

    driver.find_element(By.CSS_SELECTOR, "[data-testid='input_username']").send_keys('ajcordova@hispasat.pe')
    driver.find_element(By.CSS_SELECTOR, "[data-testid='input_password'").send_keys('123456')
    driver.find_element(By.CSS_SELECTOR, "[data-testid='button-signon-text'").click()

    time.sleep(8)


def test_user_caracteres_alfanumericos(app_config, driver: WebDriver):
    driver.get(app_config.base_url)

    wait = WebDriverWait(driver, 10)
    input_username = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_username']")))
    input_password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_password'")))

    input_username.send_keys("!$%&/()/#=?¡¿'12345567890asdQW")
    input_password.send_keys("!$%&/()/#=?¡¿'12345567890asdQW")

    loggin_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='button-signon-focus-box']")
    button_color = loggin_button.value_of_css_property("background-color")
    time.sleep(2)
    print(button_color)
    assert button_color == "rgba(255, 159, 39, 1)", f"❌ No se activó botón de login con caracteres alfanuméricos."
    print("Se aceptaron caracteres alfanuméricos en usuario")

def test_password_caracteres_alfanumericos(app_config, driver: WebDriver):
    driver.get(app_config.base_url)

    wait = WebDriverWait(driver, 10)
    input_username = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_username']")))
    input_password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_password'")))

    input_username.send_keys("!$%&/()/#=?¡¿'12345567890asdQW")
    input_password.send_keys("!$%&/()/#=?¡¿'12345567890asdQW")

    loggin_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='button-signon-focus-box']")
    button_color = loggin_button.value_of_css_property("background-color")
    time.sleep(2)
    print(button_color)
    assert button_color == "rgba(255, 159, 39, 1)", f"❌ No se activó botón de login con caracteres alfanuméricos."
    print("Se aceptaron caracteres alfanuméricos en contraseña")


def test_boton_login (app_config, driver: WebDriver):

    driver.get(app_config.base_url)

    wait = WebDriverWait(driver, 10)
    loggin_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='button-signon-focus-box']")))
    input_username = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_username']")))
    input_password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_password'")))

    input_username.send_keys("!$%&/()/#=?¡¿'12345567890asdQW")
    input_password.send_keys("!$%&/()/#=?¡¿'12345567890asdQW")

    button_color = loggin_button.value_of_css_property("background-color")
    button_text = driver.find_element(By.CSS_SELECTOR, "[data-testid='button-signon-text'")

    assert button_color == "rgba(255, 159, 39, 1)", f"❌ No cambio el color del botón."
    assert button_text.text.strip() == "INICIAR SESIÓN", f"❌ El botón no contiene el texto Iniciar Sesión."

    print("Botón de login validado correctamente")


def test_loading_generico (app_config, driver: WebDriver):

    driver.get(app_config.base_url)
    wait = WebDriverWait(driver, 10)

    time.sleep(3)

    #Iniciamos sesión para ver la animación de carga
    driver.find_element(By.CSS_SELECTOR, "[data-testid='input_username']").send_keys('ajcordova@hispasat.pe')
    driver.find_element(By.CSS_SELECTOR, "[data-testid='input_password'").send_keys('123456')
    driver.find_element(By.CSS_SELECTOR, "[data-testid='button-signon-text'").click()

    #animación de carga (puntos de carga)
    loading_dotted = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='Loading_Dotted'"))) #Bloque div con el contenedor de puntos
    dots_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='DotsContainer'"))) #Contenedor de puntos
    dots = dots_container.find_elements(By.TAG_NAME, "div") #dots = Cada uno de los puntos encerrados en un div
    dot_focus = "rgba(80, 80, 80, 1)"
    dot_focus_change = 0

    for i, dot in enumerate(dots, start=1):
        color = dot.value_of_css_property("background-color")
        print(f"Punto {i}: {color}")
        if color != dot_focus:
            dot_focus_change +=1
            time.sleep(0.05)

    assert dot_focus_change > 0, "Ningún punto cambió a color amarillo."
    print(f"✅ {dot_focus_change} puntos cambiaron a amarillo.")

def mantiene_sesion_cierre_forzado(app_config, driver: WebDriver): #Pendiente con conexión a api de nagra
    return none_of()

def mantiene_sesion_perdida_red(app_config, driver: WebDriver): #Pendiente con conexión a api de nagra
    return none_of()

def login_sesiones_superadas(app_config, driver: WebDriver): #Pendiente con conexión a api de nagra
    return none_of()


def test_login_cuenta_suspendida(app_config, driver: WebDriver):
    driver.get(app_config.base_url)
    wait = WebDriverWait(driver, 10)

    time.sleep(3)

    driver.find_element(By.CSS_SELECTOR, "[data-testid='input_username']").send_keys('selenium_net_suspend')
    driver.find_element(By.CSS_SELECTOR, "[data-testid='input_password']").send_keys('hispasat.lab')
    driver.find_element(By.CSS_SELECTOR, "[data-testid='button-signon-text'").click()

    #Esperar animación de carga
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='Loading_Dotted'")))
    #time.sleep(2)
    message_suspend = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='signon-error']")))

    assert message_suspend.text == "Cuenta suspendida. Por favor póngase en contacto con su operador. Error:(20002)",f"❌ Se mostró el mensaje incorrecto. Se mostro {message_suspend}"
    print("Mensaje de cuenta suspendida correcto")

def login_dispositivo_eliminado (app_config, driver: WebDriver): #Pendiente con conexión a api de nagra
    return none_of()

def login_con_otra_cuenta (app_config, driver: WebDriver): #Pendiente con conexión a api de nagra
    return none_of()


def test_cerrar_sesion_desde_configuracion (app_config, driver: WebDriver):
    driver.get(app_config.base_url)
    wait = WebDriverWait(driver, 10)

    time.sleep(2)

    login_url = "https://web-stag.hispasatprod.opentv.com/"
    home_url = "https://web-stag.hispasatprod.opentv.com/discover"

    if driver.current_url == login_url :
        driver.find_element(By.CSS_SELECTOR, "[data-testid='input_username']").send_keys('ajcordova@hispasat.pe')
        driver.find_element(By.CSS_SELECTOR, "[data-testid='input_password']").send_keys('123456')
        driver.find_element(By.CSS_SELECTOR, "[data-testid='button-signon-text']").click()
        # Esperar animación de carga
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='Loading_Dotted']")))
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "[data-testid='Loading_Dotted']")))

        #Esperar la url del home
        wait.until(EC.url_to_be(home_url))
        print(driver.get_window_size())
        print(home_url)

    else:
        raise AssertionError("❌ No se encontraron los elementos para el login")

    #Cerrar sesión
    driver.save_screenshot("debug.png")

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="username-text"]')))

    menu_user = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='userAccountDropdown']")))
    nombre_usuario = menu_user.find_element(By.CSS_SELECTOR, "[data-testid='username-text']").text


    print(f"Usuario logueado: {nombre_usuario}")
    menu_user.click()

    btn_cerrar_sesion = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Cerrar sesión')]")))
    btn_cerrar_sesion.click()

    #Vuelve a página de login
    wait.until(EC.url_to_be(login_url))

    assert driver.current_url == login_url, "❌ No se ejecutó el cierre de sesión"
    print("✅ Se cerró la sesión desde el menú del usuario > configuración")



















