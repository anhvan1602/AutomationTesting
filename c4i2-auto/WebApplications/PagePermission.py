import time

from selenium.webdriver.common.by import By

from Libraries.Framework.Paths import Paths
from Libraries.Framework.Utils import PageBase
from WebApplications.PageCommon import PageCommon


class PagePermission(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    def private_expand_feature_tree(self, levels):
        """
        Expands the tree by clicking through each level except the last.
        """
        for level in levels:
            current_xpath = f'//div[contains(@class,"tree-header") and .//*[text()="{level}"]]//*[contains(@class,"fal fa-angle")]'
            self.do_scroll_mouse_to_element(current_xpath)
            element_class = self.driver.find_element(By.XPATH, current_xpath).get_attribute("class")
            if "fa-angle-right" in element_class:
                self.click_obj(current_xpath)
            elif "fa-angle-down" in element_class:
                pass

    def private_toggle_switch(self, last_level, action):
        """
        Toggles the switch at the last level and verifies the action.
        """
        page_common = PageCommon(self.driver)
        btnSwitchToggle = (
            f'//div[contains(@class,"tree-header") and .//div[text()="{last_level}"]]//div[contains(@class,"switch-btn-toggle")]'
        )
        self.do_scroll_mouse_to_element(btnSwitchToggle)

        # Check the current state of the SwitchToggle
        verify = self.verify_checkbox_checked(btnSwitchToggle)

        # Perform the toggle action if necessary
        if (action == True and verify == False) or (action == False and verify == True):
            self.click_obj(btnSwitchToggle)
            verify_message = page_common.verify_notify_popup("Phân quyền thành công")
            assert verify_message, "Không có thông báo phân quyền thành công"

        time.sleep(1)

        # Verify the final state of the SwitchToggle
        verify_after = self.verify_checkbox_checked(btnSwitchToggle)
        assert verify_after == action, (
            f"Trạng thái SwitchToggle dự kiến là {action}, nhưng nhận được {verify_after}."
        )

    def action_permission(self, feature_path, status):
        """
        Main function to handle feature permissions and toggle switch status.
        """
        levels = feature_path.split("/")

        # Handle expanding the feature tree
        self.private_expand_feature_tree(levels[:-1])

        # Handle toggling the SwitchToggle and verifying the result
        self.private_toggle_switch(levels[-1], status)

    def navigate_to_unit(self, path_unit):
        """
        This function navigates through each level of the unit based on the path unit.
        """
        levels = path_unit.split("/")

        for level in levels[:-1]:
            current_xpath = f'//div[contains(@class,"base-tree") and .//*[text()="{level}"]]//*[contains(@class,"fal fa-angle")]'
            time.sleep(1)
            self.do_scroll_mouse_to_element(current_xpath)
            element_class = self.driver.find_element(By.XPATH, current_xpath).get_attribute("class")
            if "fa-angle-right" in element_class:
                self.click_obj(current_xpath)
            elif "fa-angle-down" in element_class:
                pass

        last_level = levels[-1]

        item_unit_xpath = (
            f'(//div[contains(@class, "list-item")]//child::*[text()="{last_level}"])[last()]'
        )
        self.do_scroll_mouse_to_element(item_unit_xpath)
        self.click_obj(item_unit_xpath)

    def verify_permission_with_xpath(self, status, xpath):
        """
        Verifies whether the element is visible based on the expected permission status.

        Args:
            self: Reference to the current class instance.
            status (bool): Expected permission status (True = element should be visible, False = element should not be visible).
            xpath (str): The XPath of the element to verify its visibility.

        Raises:
            AssertionError: If the actual visibility of the element does not match the expected status.
        """

        verify = self.check_element_visibility(xpath)
        if status:
            assert verify, "Phân quyền thất bại: Phần tử nên hiển thị nhưng không hiển thị !"
        else:
            assert not verify, "Phân quyền thất bại: Phần tử không nên hiển thị nhưng lại hiển thị !"

    def verify_permission_element_hidden(self, status, xpath):
        """
        Verifies whether the element is hidden based on its XPath.

        Args:
            self: Reference to the current class instance.
            xpath (str): The XPath of the element to verify its hidden status.

        Raises:
            AssertionError: If the actual visibility of the element is not hidden.
        """
        parent_div = f"{xpath}/../.."
        verify = self.check_button_clickable(parent_div)
        if status:
            assert verify, "Phân quyền thất bại: Phần tử nên hiển thị nhưng bị ẩn!"
        else:
            assert not verify, "Phân quyền thất bại: Phần tử không nên hiển thị nhưng lại hiển thị !"
