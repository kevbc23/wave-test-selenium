## Imports
from _pytest.fixtures import fixture
from selenium import webdriver
from tests.config import Config


def pytest_addoption(parser):
    parser.addoption(
        '--env',
        action = 'store',
        help = 'Ambiente de ejecución de pruebas [qa, dev]'
    )

@fixture(params=["chrome", "edge"])
def driver(request):
    if request.param == "chrome":
        op = webdriver.ChromeOptions()
        op.add_argument('--headless')
        driver = webdriver.Chrome(options=op)
        #driver = webdriver.Chrome()
    elif request.param == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError("Navegador no soportado")

    driver.maximize_window()
    yield driver
    driver.quit()

@fixture(scope = 'session')
def env(request):
    return request.config.getoption('--env')

@fixture(scope='session')
def app_config(env):
    cfg = Config(env)
    return cfg