import platform
from Libraries.Framework.Paths import Paths
from Libraries.Config import Default
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


def get_chrome_driver_win_os_hbr():
    """Headless Browser - Jenkins"""
    chrome_driver_path = os.path.join(Paths().get_path_drivers(), 'chromedriver.exe')

    # Khởi tạo options và đặt kích thước màn hình
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f'--window-size={Default.windowSize}')
    service = ChromeService(chrome_driver_path)

    return webdriver.Chrome(service=service, options=options)


def get_chrome_driver_win_os():
    """UI - debug"""
    chrome_driver_path = os.path.join(Paths().get_path_drivers(), 'chromedriver.exe')
    service = ChromeService(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


def get_chrome_driver_mac_os():
    # Khởi tạo options và đặt kích thước màn hình
    options = Options()
    # Kiểm tra nếu thuộc tính `headlessBrowser` không tồn tại hoặc là False
    if Default.headlessBrowser:
        options.add_argument('--headless')

    # options.add_argument(Default.windowSize)

    # Khởi tạo service cho Chrome Driver
    service = Service(ChromeDriverManager().install())

    # Truyền options vào webdriver.Chrome
    driver = webdriver.Chrome(service=service, options=options)

    # Phóng to trình duyệt
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
