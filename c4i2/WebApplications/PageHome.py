from Libraries.Framework.Utils import PageBase
from PageObjects.Web.Obj_PageLogin import PageLogin


class LoginPage(PageBase):
    def __init__(self, driver):
        super().__init__(driver)

    def do_login(self, username, password):
        objPageLogin = PageLogin()
        self.sendKeyInput(objPageLogin.txtUsername, username)
        self.sendKeyInput(objPageLogin.txtPassword, password)
        self.clickObj(objPageLogin.btnLogin)
