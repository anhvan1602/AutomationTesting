from Libraries.Framework.Utils import PageBase
import time

from PageObjects.Web.Obj_PageBanDo import Obi_PageBanDo
from PageObjects.Web.Obj_PageHome import Obj_PageHome
from PageObjects.Web.Obj_PageQuanLyVuViec import Obj_PageQuanLyVuViec
from PageObjects.Web.Obj_PageThietLapHeThong import Obj_PageThietLapHeThong


class PagePhanQuyen(PageBase):
    def __init__(self, driver):
        super().__init__(driver)

    def do_dangXuat(self):
        self.clickObj(Obj_PageHome.btnThongTinCaNhan)
        time.sleep(1)
        self.clickObj(Obj_PageHome.btnDangXuat)
        time.sleep(1)

    def do_checkTaiNguyenVaTinhNang(self):
        self.clickObj(Obj_PageHome.iconBanDo)
        time.sleep(3)
        check = self.findPresenceElement(Obi_PageBanDo.iconTaiNguyenTinhNang)
        return check
    def do_checkTaoVuViec(self):
        self.clickObj(Obj_PageHome.iconQuanLyVuViec)
        time.sleep(3)
        check = self.findPresenceElement(Obj_PageQuanLyVuViec.iconTaoVuViec)
        return check

