import platform
from Libraries.Config import Default
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_chrome_driver_win_os_hbr():
    """Headless Browser - Jenkins"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f'--window-size={Default.windowSize}')
    service = ChromeService(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)


def get_chrome_driver_win_os():
    """UI - debug"""
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


def get_chrome_driver_mac_os():
    options = Options()
    if Default.headlessBrowser:
        options.add_argument('--headless')
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    return driver


def get_firefox_driver_mac_os():
    return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


def get_firefox_driver_win_os():
    return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


def get_chrome_driver():
    system = platform.system()
    if system == 'Darwin':
        return get_chrome_driver_mac_os()
    elif system == 'Windows':
        if not hasattr(Default, 'headlessBrowser') or not Default.headlessBrowser:
            return get_chrome_driver_win_os()
        else:
            return get_chrome_driver_win_os_hbr()
    else:
        print(f"OS: {system} is not supported")


def get_firefox_driver():
    system = platform.system()
    if system == 'Darwin':
        return get_firefox_driver_mac_os()
    elif system == 'Windows':
        return get_firefox_driver_win_os()
