from datetime import datetime
import unittest
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from Libraries.Config import Default

from Libraries.Framework.Paths import BasePaths


class PageBase:

    def __init__(self, driver):
        self.driver = driver
        self.delay = 10

        # check languages

    def checkLanguages(self):
        self.clickObj('//*[contains(@class,"text-container")]')
        flag = Default.defaultLanguage
        # Kiểm tra ngôn ngữ, thay đổi nếu không phải là ngôn ngữ mặc định
        if self.findPresenceElement(
                f'(//*[contains(text(),"{flag}")]/../../div)//child::i[contains(@class,"fa-check")]'):
            pass
        else:
            self.clickObj(f'//div[text()="{flag}"]')
        self.clickObj('/html/body')

    def controlLabel(self):
        flag = Default.defaultLanguage
        if flag == 'Tiếng Việt':
            Label = 'Label_VI'
        elif flag == 'English':
            Label = 'Label_EN'
        return Label

    def checkButton(self, textbtn):
        Btn = '//button[.//span[text()="{}"]]'.format(textbtn)
        AriaDisabled = self.driver.find_element('xpath', Btn).get_attribute("aria-disabled")
        time.sleep(1)
        if "false" in AriaDisabled:
            # trả về true nếu button cho phép click
            return True
        else:
            return False

    def showOverlayText(self, text):
        # Thực hiện kịch bản JavaScript để chèn phần tử div mới vào trong phần tử body của trang web
        self.driver.execute_script('''
                // Tạo phần tử div mới
                var overlay = document.createElement("div");

                // Đặt kiểu dáng cho phần tử
                overlay.style.position = "fixed";
                overlay.style.top = "50%";
                overlay.style.left = "50%";
                overlay.style.transform = "translate(-50%, -50%)";
                overlay.style.zIndex = "9999";
                overlay.style.backgroundColor = "rgba(255, 255, 255, 0.8)";
                overlay.style.padding = "20px";
                overlay.style.fontSize = "48px";
                overlay.style.fontWeight = "bold";
                overlay.style.textAlign = "center";

                // Thêm nội dung chữ vào phần tử
                overlay.innerText = arguments[0];

                // Thêm phần tử vào body của trang web
                document.body.appendChild(overlay);
            ''', text)
        # Tạm dừng chương trình để phần tử hiển thị trên trình duyệt
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div")))

    def removeOverlayText(self):
        # Lấy đối tượng div đã tạo bằng id
        overlay = self.driver.find_element(By.CSS_SELECTOR, "div[style*='z-index: 9999']")

        # Thực thi JavaScript để xóa đối tượng div
        self.driver.execute_script("arguments[0].remove()", overlay)

    def reloadAndWaitAllElements(seft, timeout=5):
        seft.driver.refresh()  # tải lại trang web
        # nếu load gặp trang lỗi thì load lại
        while True:
            try:
                WebDriverWait(seft.driver, timeout).until(EC.presence_of_all_elements_located)
                seft.driver.find_element(By.XPATH, "//h3[contains(text(),'An error occur')]")
                seft.driver.refresh()
            except:
                break

    def findPresenceElement(self, txtXpath):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, txtXpath)))
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def clickObj(self, txtXpath):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, txtXpath))).click()
            count = 0
            while True:
                try:
                    # Kiểm tra lỗi CSS
                    WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Có lỗi xảy ra')]")))
                    # Tải lại trang web nếu có lỗi CSS
                    self.driver.refresh()
                    count += 1
                except:
                    break
            # Nếu có tải lại trang, in giá trị của count
            if count > 0:
                print(f"Đã tải lại trang {count} lần")

        except (NoSuchElementException, TimeoutException):
            screenshot_path = self.saveScreenShot("clickObj")
            print(f"Khong tim thay phan tu xpath sau: {txtXpath}\n{self.getImageHtml(screenshot_path)}")
            # raise unittest.TestCase.failureException("Failed to click element")

    def sendKeyInput(self, txtXpath, val):
        try:
            time.sleep(1)
            actions = ActionChains(self.driver)
            input_field = self.driver.find_element('xpath', txtXpath)
            input_field.clear()
            actions.double_click(input_field).perform()
            actions.send_keys(Keys.DELETE)
            actions.perform()
            WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, txtXpath))).send_keys(
                val)
        except (NoSuchElementException, TimeoutException):
            screenshot_path = self.saveScreenShot("sendKeyInput")
            print(f"Khong tim thay phan tu xpath sau: {txtXpath}\n{self.getImageHtml(screenshot_path)}")

    def countElementsByXpath(self, txtXpath):
        return len(self.driver.find_elements('xpath', txtXpath))

    def checkElementExit(self, txtXpath):
        return WebDriverWait(self.driver, self.delay).until(EC.visibility_of_element_located((By.XPATH, txtXpath)))

    def getTextElement(self, txtXpath):
        return self.checkElementExit(txtXpath).text

    def exportScreen(self, ImageName):
        screenshot_path = self.saveScreenShot(ImageName)
        print(f"\n{self.getImageHtml(screenshot_path)}")

    def saveScreenShot(self, labelError):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"error_{labelError}_{now}.png"
        filepath = ('{0}\ImageError\{1}').format(BasePaths().getPathReportForWeb(), filename)
        self.driver.save_screenshot(filepath)
        locate = f"./ImageError/{filename}"
        return locate

    def getImageHtml(self, path):
        """
        Returns HTML markup for embedding image in report
        """
        return f'<div><img src="{path}" alt="Error screenshot" style="width:300px;height:200px;"></div>'


    # Xuất report bằng HTMLTestRunner sử dụng getImageHtml này

    def getImageHtml1(self, path):
        """
        Returns HTML markup for embedding image in report
        """
        return f'''
            <div>
                <button class="view-image-btn" onclick="openImage('{path}')">View Image</button>
            </div>
            <br>
        '''
