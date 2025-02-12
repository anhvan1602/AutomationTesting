from datetime import datetime

import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import TimeoutException
import time
import os
from Libraries.Framework.Paths import Paths
from conftest import capture_screenshot_and_attach_allure
from appium.webdriver.common.appiumby import AppiumBy


class PageBase:

    def __init__(self, driver):
        self.driver = driver
        self.delay = 15
        self.pathReports = Paths().get_path_reports()

    def check_button_clickable(self, xpath):
        """
        Check the state of a button
        :param xpath: The XPath of the element
        :return: True if the button is enabled and clickable, otherwise False.
        """
        aria_disabled = self.driver.find_element('xpath', xpath).get_attribute("aria-disabled")
        time.sleep(1)
        if aria_disabled == "true":
            return False
        else:
            return True

    def check_element_visibility(self, txt_xpath, wait_time=15):
        """
        :param txt_xpath: The XPath of the element.
        :param wait_time: The maximum time to wait for the element to appear (in seconds).
        :return: True if the element is visible and exists, otherwise False.
        """
        original_wait_time = self.driver.timeouts.implicit_wait
        self.driver.implicitly_wait(0)
        try:
            WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, txt_xpath)))
            return True
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print(f"Không tìm thấy element có xpath: {txt_xpath}", str(e))
            return False
        finally:
            self.driver.implicitly_wait(original_wait_time)

    def show_overlay_text(self, text):
        """
        :param text: The text to be displayed in the overlay
        :return: Display an overlay text box on the web page.
        """
        self.driver.execute_script('''
                // Tạo phần tử div mới
                var overlay = document.createElement("div");

                // Đặt kiểu dáng cho phần tử
                overlay.style.position = "fixed";
                overlay.style.bottom = "10px";  // Đặt ở phía dưới màn hình
                overlay.style.left = "50%";   // Canh trái
                overlay.style.transform = "translateX(-50%)"; //Căn chỉnh vị trí chính xác giữa
                overlay.style.zIndex = "9999";
                overlay.style.backgroundColor = "gray";  // Màu nền
                overlay.style.color = "white";   // Màu chữ
                overlay.style.padding = "10px";
                overlay.style.fontSize = "12px";  // Kích thước chữ
                overlay.style.textAlign = "right";  // Canh phải
                overlay.style.borderRadius = "10px";  // Bo góc
                // Thêm nội dung chữ vào phần tử
                overlay.innerText = arguments[0];

                // Thêm phần tử vào body của trang web
                document.body.appendChild(overlay);
            ''', text)

    def remove_overlay_text(self):
        """
        :return: Remove the overlay text box from the web page.
        """
        overlay = self.driver.find_element(By.CSS_SELECTOR, "div[style*='z-index: 9999']")
        self.driver.execute_script("arguments[0].remove()", overlay)

    def click_obj(self, txt_xpath):
        """
        Click on an element
        :param txt_xpath: The XPath of the element.
        :return: If the element is clickable, it performs the click action.
        """
        try:
            element = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, txt_xpath)))
            element.click()
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print("Đã xảy ra lỗi:", str(e))
            pytest.fail(f"Không tìm thấy element có xpath: {txt_xpath}")

    def send_key_input(self, txt_xpath, val):
        """
        :param txt_xpath: The XPath of the element.
        :param val: The value or text
        :return: Send keys or text input to an input field or element
        """
        try:
            self.do_scroll_mouse_to_element(txt_xpath)
            time.sleep(1)
            actions = ActionChains(self.driver)
            input_field = self.driver.find_element(By.XPATH, txt_xpath)
            input_field.clear()
            actions.double_click(input_field).perform()
            actions.send_keys(Keys.DELETE)
            actions.perform()
            WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, txt_xpath))).send_keys(
                val)
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print("Đã xảy ra lỗi:", str(e))
            pytest.fail(f"Không tìm thấy element có xpath: {txt_xpath}")

    def select_key_dropdown(self, txt_xpath, val):
        """
        Select an option from a dropdown menu
        :param txt_xpath: The XPath of the dropdown menu.
        :param val: The value of the option to be selected from the dropdown.
        :return: selects the option that matches the value `val`
        """
        try:
            self.click_obj(txt_xpath)
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            actions.send_keys(Keys.DELETE).perform()
            actions.send_keys(val).perform()
            time.sleep(1)
            txt_val_select = f'//div[contains(@class,"as-dropdown-item-button") and (.//*[text()="{val}"] or text()="{val}")]'
            WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, txt_val_select))).click()
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print(f"Không tìm thấy element có xpath: {txt_xpath}")
            print("Đã xảy ra lỗi:", str(e))
            pytest.fail(f"Không thể lựa chọn giá trị: '{val}' trong Dropdown !")

    def set_val_input(self, txt_xpath, val):
        """
        :param txt_xpath: The XPath of the element.
        :param val: The value or text
        :return: Send text input to an input field
        """
        actions = ActionChains(self.driver)
        input_field = self.driver.find_element('xpath', txt_xpath)
        actions.double_click(input_field).perform()
        time.sleep(1)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        actions.send_keys(Keys.DELETE).perform()
        time.sleep(1)
        actions.send_keys(val)
        actions.perform()
        time.sleep(1)

    def count_elements_by_xpath(self, txt_xpath):
        """
        :param txt_xpath: The XPath of the element.
        :return: The number of elements found that match the XPath.
        """
        try:
            return len(self.driver.find_elements('xpath', txt_xpath))
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print("Đã xảy ra lỗi:", str(e))
            pytest.fail(f"Không tìm thấy element có xpath: {txt_xpath}")

    def get_text_element(self, txt_xpath, multiple=False):
        """
        :param txt_xpath: The XPath of the element.
        :param multiple: Boolean flag to indicate whether to retrieve text from multiple elements (default: False).
        :return: If multiple=False, returns the text of the first matching element.
        If multiple=True, returns a list of texts.
        """
        try:
            if multiple:
                elements = self.driver.find_elements(By.XPATH, txt_xpath)
                return [element.text for element in elements]
            else:
                if self.check_element_visibility(txt_xpath):
                    element = self.driver.find_element(By.XPATH, txt_xpath)
                    return element.text
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print("Đã xảy ra lỗi:", str(e))
            pytest.fail(f"Không tìm thấy element có xpath: {txt_xpath}")

    def verify_element_contains_content(self, txt_xpath):
        """
        :param txt_xpath: The XPath of the element.
        :return: True if the element contains visible content, otherwise False.
        """
        try:
            element = self.driver.find_element(By.XPATH, txt_xpath)
            if element.text.strip() == "":
                return False
            else:
                return True
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print(f"Không tìm thấy element có xpath: {txt_xpath}", str(e))
            return False

    def verify_checkbox_checked(self, txt_xpath):
        """
        Verify if the checkbox element specified by the XPath is checked.

        :param txt_xpath: The XPath of the checkbox element.
        :return: True if the checkbox is checked, False otherwise.
        """
        try:
            class_value = self.driver.find_element(By.XPATH, txt_xpath).get_attribute("class")
            time.sleep(1)
            if "checked" in class_value or "active" in class_value:
                return True
            else:
                return False
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print(f"Không tìm thấy element có xpath: {txt_xpath}", str(e))
            return False

    def do_scroll_mouse_to_element(self, txt_xpath):
        """
        :param txt_xpath: The XPath of the element.
        :return: Scroll the mouse to bring an element is brought into the visible area of the browser window
        """
        try:
            element = self.driver.find_element(By.XPATH, txt_xpath)
            action = ActionChains(self.driver)
            action.move_to_element(element).move_by_offset(20, 0).perform()
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print("Đã xảy ra lỗi:", str(e))
            pytest.fail(f"Không tìm thấy element có xpath: {txt_xpath}")

    def compare_imgage(self, name_feature, position=None, size=None):
        """
               So sánh hai hình ảnh và tạo hình ảnh thể hiện sự khác biệt giữa chúng.

               Parameters:
                   name_feature (str): Tên đặc điểm hoặc tiêu đề của hình ảnh.
                   position (tuple, optional): Vị trí của phần cần chụp (left, top). Mặc định là None.
                   size (tuple, optional): Kích thước của phần cần chụp (width, height). Mặc định là None.

               Returns:
                   bool: True nếu hai hình ảnh giống nhau, False nếu không giống nhau hoặc xảy ra lỗi.
                   Lưu kết quả vào allure report
        """
        from PIL import Image, ImageChops
        try:
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%m%d%H%M%S")

            # Hình ảnh cơ sở (Baseline images)
            name_image_expected = f"{name_feature}_expected.png"
            path_image_expected = self.get_path_folder_image(name_image_expected)
            if not os.path.exists(path_image_expected):
                self.save_screenshot(path_image_expected, position=position, size=size)

            # Hình ảnh kết quả (Result images)
            name_image_actual = f"{name_feature}_actual_{formatted_datetime}.png"
            path_image_actual = self.get_path_folder_image(name_image_actual)
            self.save_screenshot(path_image_actual, position=position, size=size)

            # Mở ảnh
            img1 = Image.open(path_image_expected)
            img2 = Image.open(path_image_actual)

            # Hình ảnh so sánh (Comparison images)
            diff_img = ImageChops.difference(img1, img2)
            # Chuyển đổi nền đen thành màu trắng bằng cách đảo ngược màu
            diff_img_inverted = ImageChops.invert(diff_img)
            diff_img_rgb = diff_img_inverted.convert('RGB')
            name_difference = f"{name_feature}_difference_{formatted_datetime}.png"
            path_image_different = self.get_path_folder_image(name_difference)

            diff_img_rgb.save(path_image_different)

            # Đính kèm hình ảnh vào allure report
            allure.attach.file(path_image_expected, name='Image Expected', attachment_type=allure.attachment_type.PNG)
            allure.attach.file(path_image_actual, name='Image Actual', attachment_type=allure.attachment_type.PNG)
            allure.attach.file(path_image_different, name='Image Different', attachment_type=allure.attachment_type.PNG)

            return diff_img_rgb.getbbox() is None

        except FileNotFoundError:
            print("Không tìm thấy tệp ảnh.")
            return False
        except Exception as e:
            print("Đã xảy ra lỗi khi so sánh ảnh:", e)
            return False

    def save_screenshot(self, filename, position=None, size=None):
        """
        :param filename: The file path where the screenshot will be saved.
        :param position: Optional tuple (x, y) representing the starting position of the screenshot.
        :param size: Optional tuple (width, height) representing the size of the screenshot.
        :return: Save a screenshot of the current state of the web page.
        """
        from PIL import Image
        self.driver.save_screenshot(filename)

        if position is not None and size is not None:
            screenshot = Image.open(filename)
            # Cắt ảnh theo vị trí và kích thước chỉ định
            screenshot = screenshot.crop((position[0], position[1], position[0] + size[0], position[1] + size[1]))
            screenshot.save(filename)

    def wait_for_page_load(self):
        """
        :return: Wait for the web page to fully load.
        """
        try:
            # Chờ cho đến khi phần tử loading biến mất
            WebDriverWait(self.driver, self.delay).until(
                EC.invisibility_of_element_located((By.XPATH, "//*[contains(@class,'loading')]"))
            )
        except TimeoutException:
            print("Timeout: Page did not load within the given time.")

    @staticmethod
    def get_path_folder_image(name_file):
        """
        :param name_file: The name of the image file.
        :return: The file path where the image will be stored.
        """
        path_folder = os.path.join(Paths().get_path_compare_image(), name_file)
        return path_folder

    @staticmethod
    def load_path_data_file_from_path(folder_name, file_name):
        """
        :param folder_name: The name of the folder
        :param file_name: The name of the file
        :return: Path of the file
        """
        try:
            path_file = os.path.join(Paths().get_path_datas(), folder_name, file_name)
            return path_file
        except Exception as e:
            print(f"Failed to load path {file_name}: {e}")

    def check_image_visibility(self, name_image, confidence=0.8):
        import pyautogui
        import io
        """
        Checks if the specified image is visible on the screen and returns True if found, False otherwise.
        Attaches the expected image and top matching images to Allure report.

        :param name_image: The filename of the image to be checked.
        :param confidence: Confidence level for image matching (default is 0.8).
        :return: True if the image is found on the screen, otherwise False.
        """
        try:
            path_image = os.path.join(Paths().get_path_datas(), "c4i2_images", name_image)

            # Attach the expected image to Allure report
            with open(path_image, "rb") as image_file:
                allure.attach(image_file.read(), name='Expected Image', attachment_type=allure.attachment_type.PNG)

            # Locate all matching regions on screen
            locations = list(pyautogui.locateAllOnScreen(path_image, confidence=confidence))

            # Extract and attach the top 3 matching images
            top_results = [
                (loc, pyautogui.screenshot(region=loc).convert('RGB'))
                for loc in locations[:3]
            ]

            if top_results:
                print(f"Number of top images found: {len(top_results)}")
                for i, (location, screenshot) in enumerate(top_results):
                    img_byte_arr = io.BytesIO()
                    screenshot.save(img_byte_arr, format='PNG')
                    img_byte_arr.seek(0)

                    # Attach the found image to Allure report
                    allure.attach(img_byte_arr.read(), name=f'Top Found Image {i + 1}',
                                  attachment_type=allure.attachment_type.PNG)

                    print(f"Top Image {i + 1} found at location: {location}")
                return True
            else:
                print("No matching images found.")
                return False

        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print(f"Error occurred while searching for image: {name_image}", str(e))
            return False

    @staticmethod
    def click_center_image(name_image, confidence=0.8):
        """
        Clicks the center of the image on the screen with the highest match confidence.

        Args:
            name_image (str): The name of the image file to locate on the screen.
            confidence (float, optional): The confidence level for the image match, ranging from 0.0 to 1.0.
                                          Higher values indicate stricter matching. Default is 0.8.

        Returns:
            bool: True if the image was found and clicked, False if the image was not found on the screen.
        """
        import pyautogui
        import os
        path_image = os.path.join(Paths().get_path_datas(), "c4i2_images", name_image)
        locations = list(pyautogui.locateAllOnScreen(path_image, confidence=confidence))
        if not locations:
            assert False
        best_location = max(locations, key=lambda loc: loc[2] * loc[3])
        center = pyautogui.center(best_location)
        pyautogui.click(center)
        assert True

    @staticmethod
    def drag_map(start_x, start_y, end_x, end_y, duration=1):
        import pyautogui
        """
        Simulates dragging the map from the start position to the end position.

        :param start_x: The starting x-coordinate.
        :param start_y: The starting y-coordinate.
        :param end_x: The ending x-coordinate.
        :param end_y: The ending y-coordinate.
        :param duration: The duration of the drag action in seconds.
        """
        pyautogui.moveTo(start_x, start_y)
        pyautogui.mouseDown()
        pyautogui.moveTo(end_x, end_y, duration=duration)
        pyautogui.mouseUp()

    @staticmethod
    def click_multiple_positions(positions, delay=0.5):
        import pyautogui
        """
        Clicks multiple positions on the screen using pyautogui.

        :param positions: A list of tuples [(x1, y1), (x2, y2), ...] representing the positions to click.
        :param delay: The delay (in seconds) between each click. Default is 0.5 seconds.
        """
        for pos in positions:
            pyautogui.click(pos[0], pos[1])
            print(f"Clicked on position {pos}")
            time.sleep(delay)


class PagebaseMobile:
    def __init__(self, driver):
        self.driver = driver
        self.delay = 15

    def click_obj(self, txt_xpath):
        """
        Click on an element on a mobile
        :param txt_xpath: The XPath of the element.
        :return: If the element is clickable, it performs the click action.
        """
        try:
            element = WebDriverWait(self.driver, self.delay).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, txt_xpath)))
            element.click()
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print("Đã xảy ra lỗi:", str(e))
            pytest.fail(f"Không tìm thấy element có xpath: {txt_xpath}")

    def send_key_input(self, txt_xpath, val):
        """
        :param txt_xpath: The XPath of the element on a mobile.
        :param val: The value or text
        :return: Send keys or text input to an input field or element
        """
        try:
            input_field = self.driver.find_element(AppiumBy.XPATH, txt_xpath)
            input_field.clear()
            WebDriverWait(self.driver, self.delay).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, txt_xpath))).send_keys(val)
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print("Đã xảy ra lỗi:", str(e))
            pytest.fail(f"Không tìm thấy element có xpath: {txt_xpath}")

    def check_element_exist(self, txt_xpath):
        """
        :param txt_xpath: The XPath of the element on a mobile.
        :return: True if the element is visible and exists, otherwise False.
        """
        try:
            WebDriverWait(self.driver, self.delay).until(EC.visibility_of_element_located((AppiumBy.XPATH, txt_xpath)))
            return True
        except Exception as e:
            capture_screenshot_and_attach_allure(self.driver, "ImageError")
            print(f"Không tìm thấy element có xpath: {txt_xpath}", str(e))
            return False
