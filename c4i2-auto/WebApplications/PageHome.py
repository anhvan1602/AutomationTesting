from Libraries.Framework.Utils import PageBase
from PageObjects.Web.Obj_PageLogin import PageLogin


class LoginPage(PageBase):
    def __init__(self, driver):
        super().__init__(driver)

    def do_login(self, username, password):
        obj_page_login = PageLogin()
        self.send_key_input(obj_page_login.txtUsername, username)
        self.send_key_input(obj_page_login.txtPassword, password)
        self.click_obj(obj_page_login.btnLogin)
