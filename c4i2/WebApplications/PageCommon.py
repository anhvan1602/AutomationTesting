import calendar
import json
import time

from Libraries.Framework.FactoryDrivers import *
from Libraries.Framework.Utils import PageBase
from Libraries.Plugins.PandasExcel import PandasExcel


class PageCommon(PageBase):
    def __init__(self, driver):
        super().__init__(driver)

    def chooseDate(self, dataValue):
        pageBase = PageBase(self.driver)

        valueDay = dataValue.day
        valueMonth = dataValue.month
        valueYear = dataValue.year

        if Default.defaultLanguage == 'English':
            valueMonthEnglish = calendar.month_name[valueMonth]
        elif Default.defaultLanguage == 'Tiếng Việt':
            valueMonthEnglish = 'Tháng ' + str(valueMonth)

        # Chọn năm/ Hiện tại chỉ được chọn năm trong khoảng 2016 - 2030
        pageBase.clickObj(f"//*[@class='current-date']//button[2]")
        pageBase.clickObj(f"//div[contains(text(),'{valueYear}')]")
        # Chọn tháng
        pageBase.clickObj(f"//*[@class='current-date']//button[1]")
        pageBase.clickObj(f"//div[contains(text(),'{valueMonthEnglish}')]")
        # Chọn ngày
        pageBase.clickObj(f"//td[not(contains(@class, 'next-month')) and not(contains(@class, 'prev-month'))]/div[text()='{valueDay}']")
        time.sleep(2)

    def checkResultPermission(self, check, case):
        if case == "ON":
            if check:
                print("Phân quyền thành công")
                assert True
            else:
                print("Phân quyền thất bại")
                assert False

        elif check == "OFF":
            if check:
                print("Phân quyền thất bại")
                assert False
            else:
                print("Phân quyền thành công")
                assert True

    def actionPermissions(self, fileName, sheetName, QuyenChucNang, Action):
        paths = BasePaths()
        pathFile = paths.getPathToDatasByFileName(fileName)
        pageBase = PageBase(self.driver)
        pe = PandasExcel(pathFile, sheetName)
        df = pe.getDataExcel()
        # duyệt qua từng hàng của DataFrame
        for index, row in df.iterrows():
            if QuyenChucNang == row['QuyenChucNang']:
                directory = json.loads(row['Directory'])
        dataParentDirectory = directory['Parent_Directory']
        dataChildDirectory = directory['Child_Directory']
        dataAction = directory[Action]

        if dataAction == "ON":
            dataAction = True
        elif dataAction == "OFF":
            dataAction = False

        # Tách tên các thư mục trong đường dẫn
        folders = dataParentDirectory.split('/')
        # Nhấn mở từng thư mục
        for folder in folders:
            pageBase.clickObj(
                f'//div[contains(@class,"tree-header") and .//*[text()="{folder}"]]//*[contains(@class,"fal fa-angle")]')
        time.sleep(1)
        # Check SwitchToogle
        btnSwitchToogle = (
            f'//div[contains(@class,"tree-header") and .//div[text()="{dataChildDirectory}"]]//div[contains(@class,"switch-toogle")]')
        classValue = self.driver.find_element('xpath', btnSwitchToogle).get_attribute("class")
        flagToggle = False
        time.sleep(1)
        if "active" in classValue:
            flagToggle = True

        if (dataAction == True and flagToggle == False) or (dataAction == False and flagToggle == True):
            pageBase.clickObj(btnSwitchToogle)
        time.sleep(2)

        print(f"Đã thiết lập quyền {dataParentDirectory}/{dataChildDirectory} trạng thái {dataAction} thành công <br>")
        pageBase.exportScreen("ImageSetPermissionSuccess")


    def actionPermissions1(self, fileName, sheetName, index):
        pageBase = PageBase(self.driver)
        paths = BasePaths()
        pathFile = paths.getPathToDatasByFileName(fileName)
        pe = PandasExcel(pathFile, sheetName)
        df = pe.getDataExcel()

        dataParentDirectory = df['Parent_Directory'][index]
        dataChildDirectory = df['Child_Directory'][index]
        dataAction = df['Action'][index]

        if dataAction == "ON":
            dataAction = True
        elif dataAction == "OFF":
            dataAction = False

        # Tách tên các thư mục trong đường dẫn
        folders = dataParentDirectory.split('/')
        # Nhấn mở từng thư mục
        for folder in folders:
            pageBase.clickObj(f'//div[contains(@class,"tree-header") and .//*[text()="{folder}"]]//*[contains(@class,"fal fa-angle")]')
            time.sleep(1)
        # Check SwitchToogle
        btnSwitchToogle = (f'//div[contains(@class,"tree-header") and .//div[text()="{dataChildDirectory}"]]//div[contains(@class,"switch-toogle")]')
        classValue = self.driver.find_element('xpath', btnSwitchToogle).get_attribute("class")
        flagToggle = False
        time.sleep(1)
        if "active" in classValue:
            flagToggle = True

        if (dataAction == True and flagToggle == False) or (dataAction == False and flagToggle == True):
            pageBase.clickObj(btnSwitchToogle)
        time.sleep(2)

        print(f"Đã thiết lập quyền {dataParentDirectory}/{dataChildDirectory} trạng thái {dataAction} thành công <br>")
        pageBase.exportScreen("ImageSetPermissionSuccess")


    def resultsOnGridList(self, fileName, sheetName):
        # Pre_Condition:
        # - Dữ lệu vừa tạo/edit
        # - Full thông tin trên danh sách lưới

        pageBase = PageBase(self.driver)
        paths = BasePaths()
        pathFile = paths.getPathToDatasByFileName(fileName)
        pe = PandasExcel(pathFile, sheetName)
        df = pe.getDataExcel()
        Label = PageBase.controlLabel(self)

        labelsearch = pe.getValByIndex(2, Label)
        valuesearch = pe.getValByIndex(2, 'Value')

        # Show full data tren grid
        pageBase.clickObj('//*[contains(@class,"fal fa-line-columns")]')
        pageBase.clickObj('//*[text()="Show all"]')
        pageBase.clickObj('/html/body')

        pageBase.sendKeyInput('//input[@name="searchKey"]', valuesearch)
        print(f"     Check '{labelsearch}' la '{valuesearch}' tren grid <br>")
        maxRow = pe.getRowDataFile(df)
        i = 0
        t = 0

        while i < maxRow:
            dataTypeOf = df['TypeOf'][i]
            dataLabel = df[Label][i]
            dataValue = df['Value'][i]
            if dataTypeOf == 'datetime':
                day = dataValue.day
                month = dataValue.month
                formatted_month = '{:02d}'.format(month)  # chuyển month thành chuỗi với định dạng 2 chữ số
                year = dataValue.year
                dataValue = f'{formatted_month}/{day}/{year}'
            match dataValue:
                case "True":
                    txtInput = '(//div[contains(@class,"boolean") and i])[1]'
                case "False":
                    txtInput = '(//div[contains(@class,"boolean")])[1]'
                case default:
                    txtInput = ('(//*[text()="{}"])[1]').format(dataValue)
            if (self.findPresenceElement(txtInput)):
                print(f"Find '{dataLabel}' is '{dataValue}' <br>")
            else:
                print(f"Find not '{dataLabel}' is '{dataValue}' <br>")
                pageBase.exportScreen("FindNotData")
                t += 1
            i += 1
            time.sleep(1)
            # nếu thêm thẻ div thông báo check trên danh sách lưới thì thêm hàm remove để bỏ thông báo khi đã check xong
        pageBase.removeOverlayText()
        return t

    def fillDataToForm(self, fileName, sheetName):
        paths = BasePaths()
        pathFile = paths.getPathToDatasByFileName(fileName)
        # print(pathFile)
        pe = PandasExcel(pathFile, sheetName)
        df = pe.getDataExcel()
        # print(df)
        pageBase = PageBase(self.driver)
        Label = pageBase.controlLabel()
        maxRow = pe.getRowDataFile(df)
        i = 0
        while i < maxRow:
            typeOf = df['TypeOf'][i]
            label = df[Label][i]
            value = df['Value'][i]
            self.fillIn(typeOf, label, value)
            i += 1
            # time.sleep(1)

    def fillIn(self, typeOf, label, val):
        match typeOf:
            case "input":
                txtInput = ('//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//input').format(label)
                self.sendKeyInput(txtInput, val)
            case "textarea":
                txtInput = ('//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//textarea').format(label)
                self.sendKeyInput(txtInput, val)
            case "dropdown":
                iconRow = ('//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//div[@class="arrow"]').format(label)
                self.clickObj(iconRow)
                time.sleep(2)
                # txtValSelect = ('//div[contains(@class,"list-item-title") and text()="{}"]').format(val)
                txtValSelect = ('//li[.//div[text()="{}"]]').format(val)
                self.clickObj(txtValSelect)
            case "dropdown_selectlayer":
                iconRow = ('//div[contains(@class,"layout-row overflow-hidden item-margin-md") and .//div[text()="{}"]]//div[@class="arrow"]').format(label)
                self.clickObj(iconRow)
                time.sleep(2)
                txtValSelect = ('//li[.//span[text()="{}"]]').format(val)
                self.clickObj(txtValSelect)
            case "switchToggle":
                btnSwitchToogle = ('//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//div[contains(@class,"switch-toogle")]').format(label)
                classValue = self.driver.find_element('xpath', btnSwitchToogle).get_attribute("class")
                flagToggle = False
                time.sleep(1)
                if "active" in classValue:
                    flagToggle = True
                if (val == "True" and flagToggle == False) or (val == "False" and flagToggle == True):
                    self.clickObj(btnSwitchToogle)
            case "checkbox":
                btnCheckbox = ('//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//span[contains(@class,"checkbox-input")]').format(label)
                classValue = self.driver.find_element('xpath', btnCheckbox).get_attribute("class")
                flagToggle = False
                time.sleep(1)
                if "checked" in classValue:
                    flagToggle = True
                if (val == "True" and flagToggle == False) or (val == "False" and flagToggle == True):
                    self.clickObj(btnCheckbox)
            case "datetime":
                btnCalendar = (f'//div[contains(@class,"form-control-label") and .//div[text()="{label}"]]//*[@class="fal fa-calendar-alt  "]')
                self.clickObj(btnCalendar)
                self.chooseDate(val)

    def verifyNotifyPopup(self, txtMessageCheckExit):
        res = False
        getTextPopup = self.getTextElement('//div[@class="toast-message css-0"]')
        if txtMessageCheckExit in getTextPopup:
            res = True
        print("\n" + getTextPopup)
        return res

    def getValueCell(self, fileName, sheetName, indexRow):
        pathFile = BasePaths().getPathToDatasByFileName(fileName)
        pe = PandasExcel(pathFile, sheetName)
        return pe.getValByIndex(indexRow, 'Value')
#
#
# if __name__ == "__main__":
#     driver = None
