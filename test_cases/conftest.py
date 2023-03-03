import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from test_data.test_data import Data

@pytest.fixture
def driver():
    if Data.browser == "chrome":
        service = ChromeService(executable_path=ChromeDriverManager().install())
        return webdriver.Chrome(service=service)
    else:
        # print("Browser type unsupported")
        # todo throw Error
        pass
