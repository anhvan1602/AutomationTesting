import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from Libraries.Framework.Paths import BasePaths
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Libraries.Config import Default
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions



def getChromeDriver_WinOS():
    return webdriver.Chrome(executable_path=os.path.join(BasePaths().getPathToDrivers(), 'chromedriver.exe'))

def getFirefoxDriver_WinOS():
    firefox_options = FirefoxOptions()
    return webdriver.Firefox(options=firefox_options)

def getFirefoxDriver_WinOS1():
    return webdriver.Firefox(executable_path=os.path.join(BasePaths().getPathToDrivers(), 'geckodriver.exe'))

def getChromeDriver_MacOS():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def getChromeDriver():
    if Default.deviceTypeID == "MacOS":
        return getChromeDriver_MacOS()
    else:
        return getFirefoxDriver_WinOS()



# Định dạng màn hình zoom 75%
# def getChromeDriver_WinOS():
#     chrome_options = Options()
#     chrome_options.add_argument("--force-device-scale-factor=0.75")
#     driver = webdriver.Chrome(executable_path=os.path.join(BasePaths().getPathToDrivers(), 'chromedriver.exe'), options=chrome_options)
#     return driver
