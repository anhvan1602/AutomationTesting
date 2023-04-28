import unittest

import pyautogui as pyautogui

from Libraries.Framework.FactoryDrivers import *
from Libraries.Framework.Utils import PageBase
from PageObjects.Web.Obj_PageHome import Obj_PageHome
from PageObjects.Web.Obj_PageThietLapHeThong import Obj_PageThietLapHeThong
from WebApplications.PagePhanQuyen import PagePhanQuyen
from WebApplications.PageCommon import PageCommon
from WebApplications.PageHome import LoginPage
from Libraries.Config import Default
import time


class TestPhanQuyen(unittest.TestCase):
    default = Default()
    url, username, password = default.url, default.username, default.password

    default = Default()
    urlSetRole, usernameSetRole, passwordSetRole = default.urlSetRole, default.usernameSetRole, default.passwordSetRole

    timeOut = default.timeOut

    # Lấy kích thước màn hình và tọa độ của nó
    screenWidth, screenHeight = pyautogui.size()
    halfScreenWidth = int(screenWidth / 2)
    halfScreenHeight = int(screenHeight / 2)

    # Tọa độ của hai màn hình
    leftScreen = (0, 0, halfScreenWidth, screenHeight)
    rightScreen = (halfScreenWidth, 0, halfScreenWidth, screenHeight)

    # Khởi tạo ChromeDriver đặt kích thước và vị trí cửa sổ
    driverChrome = getChromeDriver_WinOS()
    driverChrome.set_window_size(halfScreenWidth, screenHeight)
    driverChrome.set_window_position(leftScreen[0], leftScreen[1])

    # Khởi tạo FirefoxDriver đặt kích thước và vị trí cửa sổ
    driverFirefox = getFirefoxDriver_WinOS()
    driverFirefox.set_window_size(halfScreenWidth, screenHeight)
    driverFirefox.set_window_position(rightScreen[0], rightScreen[1])


    @classmethod
    def setUpClass(self):
        self.driverChrome.get(self.url)

        self.driverFirefox.get(self.urlSetRole)
        pageLogin = LoginPage(self.driverFirefox)
        pageLogin.do_login(self.usernameSetRole, self.passwordSetRole)
        time.sleep(4)

        # Thao tác chuyển trình duyệt Firefox đến trang phân quyền
        pageBase = PageBase(self.driverFirefox)

        pageBase.clickObj(Obj_PageHome.btnThongTinCaNhan)
        time.sleep(1)
        pageBase.clickObj(Obj_PageHome.btnThietLapHeThong)
        time.sleep(1)
        pageBase.clickObj(Obj_PageThietLapHeThong.tabVaiTro)
        time.sleep(1)
        pageBase.clickObj(Obj_PageThietLapHeThong.btnPhanQuyen)
        time.sleep(1)

        self.fileName = "c4i2_v1_0_1.xlsx"
        self.sheetName = "CheckPhanQuyen"

    # def setUpAndCheckPermissions(self, QuyenChucNang, Action, Check):
    #     # Set phân quyền
    #     pageBase = PageBase(self.driverFirefox)
    #     pageCommon = PageCommon(self.driverFirefox)
    #     pageCommon.actionPermissions(self.fileName, self.sheetName, QuyenChucNang, Action)
    #     time.sleep(2)
    #     pageBase.clickObj(Obj_PageThietLapHeThong.btnDongToanBo)
    #
    #     # Check phân quyền
    #     pageLogin = LoginPage(self.driverChrome)
    #     pageLogin.do_login(self.username, self.password)
    #     pageBase = PageBase(self.driverChrome)
    #     pagePhanQuyen = PagePhanQuyen(self.driverChrome)
    #     check = Check
    #     pageBase.exportScreen("checkPermission")
    #     pagePhanQuyen.do_dangXuat()
    #     pageCommon = PageCommon(self.driverChrome)
    #     pageCommon.checkResultPermission(check, Action)
    #
    # def test_checkOnCreateVuViec1(self):
    #     self.step = ["Pre_Condition: ",
    #                  "Step 1: ",
    #                  "Step 2: ",
    #                  "Step 3: ",
    #                  "Step 4: ",
    #                  "Step 5: ",
    #                  "Step 6: ",
    #                  "Expected Results: "]
    #     Action = "ActionON"
    #     QuyenChucNang = "VỤ VIỆC/QUẢN LÝ"
    #     pagePhanQuyen = PagePhanQuyen(self.driverChrome)
    #     self.setUpAndCheckPermissions(QuyenChucNang, Action, Check=pagePhanQuyen.do_checkTaoVuViec())

    def test_checkOnTaiNguyenVaTinhNang(self):
        self.step = ["Pre_Condition: ",
                     "Step 1: ",
                     "Step 2: ",
                     "Step 3: ",
                     "Step 4: ",
                     "Step 5: ",
                     "Step 6: ",
                     "Expected Results: "]

        Action = "ActionON"
        QuyenChucNang = "TÀI NGUYÊN VÀ TÍNH NĂNG"

        # Set phân quyền bật Xem Tài Nguyên Và Tính Năng
        pageBase = PageBase(self.driverFirefox)
        pageCommon = PageCommon(self.driverFirefox)
        pageCommon.actionPermissions(self.fileName, self.sheetName, QuyenChucNang, Action)
        time.sleep(2)
        pageBase.clickObj(Obj_PageThietLapHeThong.btnDongToanBo)

        # Check phân quyền
        pageLogin = LoginPage(self.driverChrome)
        pageLogin.do_login(self.username, self.password)
        pageBase = PageBase(self.driverChrome)
        pagePhanQuyen = PagePhanQuyen(self.driverChrome)
        check = pagePhanQuyen.do_checkTaiNguyenVaTinhNang()
        pageBase.exportScreen("checkOnVuViecPass")
        pagePhanQuyen.do_dangXuat()
        pageCommon = PageCommon(self.driverChrome)
        pageCommon.checkResultPermission(check, Action)

    def test_checkOffTaiNguyenVaTinhNang(self):
        self.step = ["Pre_Condition: ",
                     "Step 1: ",
                     "Step 2: ",
                     "Step 3: ",
                     "Step 4: ",
                     "Step 5: ",
                     "Step 6: ",
                     "Expected Results: "]
        Action = "ActionOFF"
        QuyenChucNang = "TÀI NGUYÊN VÀ TÍNH NĂNG"

        # Set phân quyền bật Xem Tài Nguyên Và Tính Năng
        pageBase = PageBase(self.driverFirefox)
        pageCommon = PageCommon(self.driverFirefox)
        pageCommon.actionPermissions(self.fileName, self.sheetName, QuyenChucNang, Action)
        time.sleep(2)
        pageBase.clickObj(Obj_PageThietLapHeThong.btnDongToanBo)

        # Check phân quyền
        pageLogin = LoginPage(self.driverChrome)
        pageLogin.do_login(self.username, self.password)
        pageBase = PageBase(self.driverChrome)
        pagePhanQuyen = PagePhanQuyen(self.driverChrome)
        check = pagePhanQuyen.do_checkTaiNguyenVaTinhNang()
        pageBase.exportScreen("checkOnVuViecPass")
        pagePhanQuyen.do_dangXuat()
        pageCommon = PageCommon(self.driverChrome)
        pageCommon.checkResultPermission(check, Action)

    def test_checkOnCreateVuViec(self):
        self.step = ["Pre_Condition: ",
                     "Step 1: ",
                     "Step 2: ",
                     "Step 3: ",
                     "Step 4: ",
                     "Step 5: ",
                     "Step 6: ",
                     "Expected Results: "]
        Action = "ActionON"
        QuyenChucNang = "VỤ VIỆC/QUẢN LÝ"

        # Set phân quyền bật Xem Tài Nguyên Và Tính Năng
        pageBase = PageBase(self.driverFirefox)
        pageCommon = PageCommon(self.driverFirefox)
        pageCommon.actionPermissions(self.fileName, self.sheetName, QuyenChucNang, Action)
        time.sleep(2)
        pageBase.clickObj(Obj_PageThietLapHeThong.btnDongToanBo)

        # Check phân quyền
        pageLogin = LoginPage(self.driverChrome)
        pageLogin.do_login(self.username, self.password)
        pageBase = PageBase(self.driverChrome)
        pagePhanQuyen = PagePhanQuyen(self.driverChrome)
        check = pagePhanQuyen.do_checkTaoVuViec()
        pageBase.exportScreen("checkOnVuViecPass")
        pagePhanQuyen.do_dangXuat()
        pageCommon = PageCommon(self.driverChrome)
        pageCommon.checkResultPermission(check, Action)


    def test_checkOffCreateVuViec(self):
        Action = "ActionOFF"
        self.step = ["Pre_Condition: ",
                     "Step 1: ",
                     "Step 2: ",
                     "Step 3: ",
                     "Step 4: ",
                     "Step 5: ",
                     "Step 6: ",
                     "Expected Results: "]
        QuyenChucNang = "VỤ VIỆC/QUẢN LÝ"

        # Set phân quyền bật Xem Tài Nguyên Và Tính Năng
        pageBase = PageBase(self.driverFirefox)
        pageCommon = PageCommon(self.driverFirefox)
        pageCommon.actionPermissions(self.fileName, self.sheetName, QuyenChucNang, Action)
        time.sleep(2)
        pageBase.clickObj(Obj_PageThietLapHeThong.btnDongToanBo)

        # Check phân quyền
        pageLogin = LoginPage(self.driverChrome)
        pageLogin.do_login(self.username, self.password)
        pageBase = PageBase(self.driverChrome)
        pagePhanQuyen = PagePhanQuyen(self.driverChrome)
        check = pagePhanQuyen.do_checkTaoVuViec()
        pageBase.exportScreen("checkOnVuViecPass")
        pagePhanQuyen.do_dangXuat()
        pageCommon = PageCommon(self.driverChrome)
        pageCommon.checkResultPermission(check, Action)


    @classmethod
    def tearDownClass(self):
        self.driverChrome.quit()
        self.driverFirefox.quit()



if __name__ == "__main__":
    unittest.main(verbosity=2)
