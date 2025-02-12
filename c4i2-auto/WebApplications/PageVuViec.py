import os
import time

from Libraries.Framework.Paths import Paths
from WebApplications.PageCommon import PageCommon, FillData
from Libraries.Framework.Utils import PageBase
from selenium.webdriver.common.by import By


class CaseManagement(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    def do_dien_thong_tin_vu_viec(self, data):
        fill_data = FillData(self.driver)
        fill_data.fill_in_each_attribute(data)

    def do_dien_thong_tin_doi_tuong(self, data_update_obj):
        for item in data_update_obj:
            type_of = item["TypeOf"]
            label = item["Label"]
            value = item["Value"]
            self.private_fill_media(type_of, label, value)

    def do_them_thong_tin_file_dinh_kem(self, data_update_attach_file):
        for item in data_update_attach_file:
            type_of = item["TypeOf"]
            label = item["Label"]
            value = item["Value"]
            self.private_fill_media(type_of, label, value)

    def private_fill_media(self, type_of, label, val):
        res = False
        if type_of == "ID":
            value = str(val)
            attribute = "CMND/ CCCD/ Hộ chiếu"
            btn_them_doi_tuong = '(//span[contains(text(),"Thêm")])[1]'
            bnt_edit_doi_tuong = (
                '//div[contains(@class,"section-header") and ./h3[text()="{0}"]]//i[contains(@class,"fal fa-pencil-alt ")]').format(
                label)
            input_id_doi_tuong = (
                '//div[contains(@class,"popup")]//div[contains(@class,"form-control-label") and .//div[text()="{0}"]]//input').format(
                attribute)
            btn_tra_cuu_doi_tuong = (
                '(//div[contains(@class,"form-control-label") and .//div[text()="CMND/ CCCD/ Hộ chiếu"]])//child::i[contains(@class, "fal fa-file-search")]').format(
                attribute)
            label_doi_tuong = "Đối tượng"
            bnt_chon_doi_tuong = f'//div[contains(@class, "dg-row")]//child::div[text()="{label_doi_tuong}"]'
            label_cap_nhat_doi_tuong = "Cập nhật đối tượng"
            bnt_cap_nhat_doi_tuong = f'//button[.//span[text()="{label_cap_nhat_doi_tuong}"]]'
            btn_xac_nhan = '//span[text()="Xác nhận"]'
            self.click_obj(btn_them_doi_tuong)
            self.click_obj(bnt_edit_doi_tuong)
            time.sleep(2)
            self.send_key_input(input_id_doi_tuong, value)
            time.sleep(2)
            self.click_obj(btn_tra_cuu_doi_tuong)
            time.sleep(2)
            self.click_obj(bnt_chon_doi_tuong)
            time.sleep(2)
            self.click_obj(bnt_cap_nhat_doi_tuong)
            time.sleep(2)
            self.click_obj(btn_xac_nhan)
            time.sleep(3)
            res = True
        if type_of == "Image":
            btn_them_doi_tuong = '(//span[contains(text(),"Thêm")])[1]'
            bnt_edit_doi_tuong = (
                '//div[contains(@class,"section-header") and ./h3[text()="{0}"]]//i[contains(@class,"fal fa-pencil-alt ")]').format(
                label)
            bnt_tra_cuu_nhan_dang_doi_tuong = '//button[.//span[text()="Tra cứu nhận dạng"]]'
            bnt_cap_nhat_doi_tuong = '//button[.//span[text()="Cập nhật đối tượng"]]'
            bnt_chon_doi_tuong_dau_tien = (
                '((//div[contains(@class,"popup-container") and //*[text()="Nhận dạng đối tượng"]])//child::span[text()="{0}"])[1]').format(
                "Chọn")
            self.click_obj(btn_them_doi_tuong)
            self.click_obj(bnt_edit_doi_tuong)
            # pathImage = ('{0}\c4i2_images\{1}').format(BasePaths().getPathToDatas(), val)
            path_image = os.path.join(self.pathDatas, "c4i2_images", val)
            self.driver.find_element(By.XPATH, '//div[text()="Ảnh chính"]/..//input[@type="file"]').send_keys(path_image)
            time.sleep(2)
            self.click_obj(bnt_tra_cuu_nhan_dang_doi_tuong)
            time.sleep(2)
            self.click_obj(bnt_chon_doi_tuong_dau_tien)
            time.sleep(2)
            self.click_obj(bnt_cap_nhat_doi_tuong)
            time.sleep(3)
            res = True

        if type_of == "Media":
            for item in val:
                path_image = os.path.join(self.pathDatas, "c4i2_images", item)
                str_xpath_element = '//div[contains(@class,"upload-files-container") and .//*[text()="{0}"]]//input[@type="file"]'.format(
                    label)
                self.driver.find_element(By.XPATH, str_xpath_element).send_keys(path_image)
            # time.sleep(10)
            res = True

        return res


class CaseManagementTabVuViec(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    def do_verify_result_search_in_popup(self, type_of, label, value):
        if type_of in ["input"]:
            txt_input = f'//div[contains(text(), "{label}")]//ancestor::div[contains(@class, "form")]//child::input[contains(@value, "{value}")]'
        elif type_of in ["dropdown-btn-text", "textarea"]:
            txt_input = f'//div[contains(text(), "{label}")]//ancestor::div[contains(@class, "form")]//child::div[contains(text(), "{value}")]'
        else:
            txt_input = None
        if txt_input is not None:
            if self.check_element_visibility(txt_input):
                print(f"Tìm thấy '{label}' là '{value}' trong popup chi tiết")
                return True
            else:
                print(f"Không tìm thấy '{label}' là '{value}' trong popup chi tiếc")
                return False

    def do_verify_data_cleaned(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        reset_data = element.get_attribute('value')
        if reset_data == '':
            print("Test Passed: Dữ liệu đã nhập bị xóa thành công")
            return True
        else:
            print("Test Failed: Dữ liệu đã nhập không bị xóa")
            return False

    def do_verify_time_range_case(self, attribute, from_time, to_time, value_actual=None):
        page_common = PageCommon(self.driver)
        result_compare = page_common.do_get_data_test_in_grid(attribute)
        if value_actual is None:
            value_actual = 0
        result_compare = [item[value_actual] for item in result_compare if len(item) > value_actual]
        page_common = PageCommon(self.driver)
        from_time = page_common.format_datetime(from_time)
        to_time = page_common.format_datetime(to_time)
        result_compare = page_common.format_datetime(result_compare)
        verify = page_common.is_valid_tim_range(result_compare, from_time, to_time)

        return verify
