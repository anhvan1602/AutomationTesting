import unittest
from Libraries.Framework.FactoryDrivers import *
from WebApplications.PageHome import LoginPage
from Libraries.Config import Default
import time


class TestCaseEx(unittest.TestCase):
    defaultTenant = Default()
    url = defaultTenant.url
    username = defaultTenant.username
    password = defaultTenant.password
    timeOut = defaultTenant.timeOut


    @classmethod
    def setUpClass(cls):
        cls.driver = getFirefoxDriver_WinOS()
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()
        cls.driver.get(cls.url)

        # pageLogin = LoginPage(cls.driver)
        # pageLogin.do_login(cls.username, cls.password)
        time.sleep(2)

    def test_creEx(self):
        self.step = ["Pre_Condition: ",
                     "Step 1: ",
                     "Step 2: ",
                     "Step 3: ",
                     "Step 4: ",
                     "Step 5: ",
                     "Step 6: ",
                     "Expected Results: "]



    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
