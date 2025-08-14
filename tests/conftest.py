## Imports
from _pytest.config import hookimpl
from _pytest.fixtures import fixture
from selenium import webdriver
from tests.config import Config
import time


def pytest_addoption(parser):
    parser.addoption(
        '--env',
        action = 'store',
        help = 'Ambiente de ejecución de pruebas [qa, dev]'
    )

@fixture(params=["chrome", "edge"])
def driver(request):
    if request.param == "chrome":
        # op = webdriver.ChromeOptions()
        # op.add_argument('--headless')
        # driver = webdriver.Chrome(options=op)
        driver = webdriver.Chrome()
    elif request.param == "edge":
        op = webdriver.EdgeOptions()
        op.add_argument("--headless=new")
        op.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(options=op)
        #driver = webdriver.Chrome()
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

@hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    global start_time
    start_time = time.time()

@hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    total_time = time.time() - start_time
    minutes, seconds = divmod(total_time, 60)
    print(f"\n⏱ Tiempo total de ejecución: {int(minutes)} min {seconds:.2f} seg")