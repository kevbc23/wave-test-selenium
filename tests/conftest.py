## Imports
from _pytest.config import hookimpl
from _pytest.fixtures import fixture
from selenium import webdriver
from tests.config import Config
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions



def pytest_addoption(parser):
    parser.addoption(
        '--env',
        action = 'store',
        help = 'Ambiente de ejecución de pruebas [qa, dev]'
    )

@fixture(params=["chrome", "edge"])
def driver(request):
    if request.param == "chrome":
        # options = ChromeOptions()
        # options.add_argument("--headless=new")  # Activa modo Headless
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        # driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome() ##Descomentar para habilitar vista de navegador


    elif request.param == "edge":
        options = EdgeOptions()
        options.add_argument("--headless=new")  # Activa modo Headless
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Edge(options=options)
        #driver = webdriver.Edge() ##Descomentar para habilitar vista de navegador

    driver.set_window_size(1920, 1080)  # Forzamos por si acaso
    yield driver
    driver.quit()

@fixture(scope = 'session')
def env(request):
    return request.config.getoption('--env')

@fixture(scope='session')
def app_config(env):
    cfg = Config(env)
    return cfg

@hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    global start_time
    start_time = time.time()

@hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    total_time = time.time() - start_time
    minutes, seconds = divmod(total_time, 60)
    print(f"\n⏱ Tiempo total de ejecución: {int(minutes)} min {seconds:.2f} seg")