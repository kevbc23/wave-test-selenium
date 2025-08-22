import time

import webcolors
from pytest import mark
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import none_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.PageObject.Pages.HomePage import HomePage
from tests.conftest import app_config


def test_logo_de_app (app_config, driver:WebDriver):
    driver.get(app_config.base_url)
    home = HomePage(driver)

    logo_div = home.wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[style*='icon_logo.webp']"))
    )
    # Extraer medidas del logo
    size = logo_div.size
    width = size['width']
    height = size['height']

    print(f"📐  Medidas del logo -> Ancho: {width}px, Alto: {height}px")

    # Validar medidas esperadas
    assert width == 155, f"❌ El ancho esperado era 155px pero se obtuvo {width}px"
    assert height == 97, f"❌ El alto esperado era 96px pero se obtuvo {height}px"

    home.login("ajcordova@hispasat.pe", "123456")

    home_url = "https://web-stag.hispasatprod.opentv.com/discover"
    home.wait.until(EC.url_to_be(home_url))

    #Iteramos en cada menú

    menus = [
        "//div[contains(text(),'INICIO')]",
        "//div[contains(text(),'GUÍA')]",
        "//div[contains(text(),'MIS CONTENIDOS')]",
        "//div[@aria-label='settings']//*[name()='svg']"
    ]

    for menu in menus:
        boton = home.wait.until(EC.element_to_be_clickable((By.XPATH, menu)))
        boton.click()

        logo_div = home.wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[style*='icon_logo.webp']"))
        )
        # Extraer medidas del logo
        size = logo_div.size
        width = size['width']
        height = size['height']

        print(f"📐  Medidas del logo -> Ancho: {width}px, Alto: {height}px")

        assert width == 93, f"❌ El ancho esperado era 155px pero se obtuvo {width}px"
        assert height == 58, f"❌ El alto esperado era 96px pero se obtuvo {height}px"


    print("✅ Validación correcta: las medidas del logo en todos los menús coinciden con lo esperado.")

def closest_color(requested_color):
    min_colors = {}
    for name in webcolors.names("css3"):   # lista de colores CSS3
        r_c, g_c, b_c = webcolors.hex_to_rgb(webcolors.name_to_hex(name))
        diff = (r_c - requested_color[0]) ** 2 + (g_c - requested_color[1]) ** 2 + (b_c - requested_color[2]) ** 2
        min_colors[diff] = name
    return min_colors[min(min_colors.keys())]


def test_color_focus (app_config, driver:WebDriver):
    driver.get(app_config.base_url)
    home = HomePage(driver)

    loggin_button = home.wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='button-signon-focus-box']")))
    input_username = home.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_username']")))
    input_password = home.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='input_password'")))

    input_username.send_keys("ajcordova@hispasat.pe")
    input_password.send_keys("123456")

    button_color = loggin_button.value_of_css_property("background-color")

    rgba = button_color.replace("rgba(", "").replace("rgb(", "").replace(")", "").split(",")
    r, g, b = [int(x.strip()) for x in rgba[:3]]  # solo RGB
    try:
        color_name = webcolors.rgb_to_name((r, g, b))
    except ValueError:
        color_name = str.capitalize(closest_color((r, g, b)))
    print(f"✅ El color de focus identificado es: {color_name} ({r},{g},{b})")

    assert color_name is not None, "❌ No se pudo identificar el color del focus"


def test_menuprincipal_inicio (app_config, driver: WebDriver):
    driver.get(app_config.base_url)
    home = HomePage(driver)

    menu_inicio = home.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'INICIO')]")))
    menu_guia = home.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'GUÍA')]")))
    menu_contenidos = home.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'MIS CONTENIDOS')]")))

