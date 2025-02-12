import json
import random
import string
from datetime import datetime
import os
import xml.etree.ElementTree as elementTree
import xml.dom.minidom

from Libraries.Framework.Paths import Paths


class JsonDataHandler:
    def __init__(self, data):
        """
        Khởi tạo một đối tượng DataHandler với dữ liệu được truyền vào.
        Parameters:
            data (list): Danh sách các phần tử dữ liệu từ file JSON.
        """
        self.data = data

    def get_value_by_label(self, label):
        """
        Trả về giá trị tương ứng với một nhãn (label) cho trước.
        Parameters:
            label (str): Nhãn cần tìm giá trị.
        Returns:
            str or None: Giá trị của nhãn nếu được tìm thấy, None nếu không tìm thấy.
        """
        for item in self.data:
            if item["Label"] == label:
                return item["Value"]
        return None

    def get_info_by_label(self, label):
        """
        Trả về TypeOf, Label và Value tương ứng với một nhãn (label) cho trước.
        Parameters:
            label (str): Nhãn cần tìm thông tin.
        Returns:
            tuple or None: Tuple chứa TypeOf, Label và Value nếu được tìm thấy, None nếu không tìm thấy.
        """
        for item in self.data:
            if item["Label"] == label:
                return item["TypeOf"], item["Label"], item["Value"]
        return None

    def get_info_by_type_of(self, typeof):
        """
        Trả về TypeOf, Label và Value tương ứng với một loại (typeof) cho trước.
        Parameters:
            typeof (str): Nhãn cần tìm thông tin.
        Returns:
            tuple or None: Tuple chứa TypeOf, Label và Value nếu được tìm thấy, None nếu không tìm thấy.
        """
        for item in self.data:
            if item["TypeOf"] == typeof:
                return item["TypeOf"], item["Label"], item["Value"]
        return None

    def filter_data_by_type(self, data_type):
        """
        Lọc và trả về các phần tử dữ liệu có loại (type) tương ứng.
        Parameters:
            data_type (str): Loại dữ liệu cần lọc.
        Returns:
            list: Danh sách các phần tử dữ liệu có loại (type) tương ứng.
        """
        filtered_data = []
        for item in self.data:
            if item["TypeOf"] == data_type:
                filtered_data.append(item)
        return filtered_data

    def modify_value_by_label(self, label, new_value):
        """
        Sửa đổi giá trị của một nhãn (label) cho trước thành giá trị mới.
        Parameters:
            label (str): Nhãn cần sửa đổi giá trị.
            new_value (str): Giá trị mới cần gán.
        Returns:
            bool: True nếu sửa đổi thành công, False nếu không tìm thấy nhãn tương ứng.
        """
        for item in self.data:
            if item["Label"] == label:
                item["Value"] = new_value
                return True
        return False


class DataGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_random_data(data_type):
        """Tạo dữ liệu ngẫu nhiên dựa trên loại dữ liệu yêu cầu."""
        if data_type == "number":
            return ''.join(random.choices(string.digits, k=10))
        elif data_type == "string":
            return ''.join(random.choices(string.ascii_letters, k=10))
        elif data_type == "alphanumeric":
            return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        elif data_type == "datetime":
            return datetime.now().strftime("%d%m%Y%H%M")
        elif data_type.startswith("custom_"):  # Nếu data_type bắt đầu bằng "custom_", xử lý theo mẫu "tùy chỉnh_ddmmyy"
            current_time = datetime.now().strftime('%d%m_%H%M')
            random_letters = ''.join(random.choices(string.ascii_letters, k=2))
            return f"{data_type[7:]}_{current_time}_{random_letters}"
        else:
            raise ValueError("Unknown data type")

    @staticmethod
    def update_json_value(file_path, path, data_type):
        """
        Cập nhật giá trị trong file JSON tại đường dẫn phân cấp đã cho.

        :param file_path: Đường dẫn đến file JSON.
        :param path: Đường dẫn phân cấp đến dữ liệu cần chỉnh sửa (dạng list).
        :param data_type: Loại dữ liệu để tạo dữ liệu ngẫu nhiên (number, string, alphanumeric, datetime).
        :return: Tuple (updated, error_message) với updated là True nếu cập nhật thành công, False nếu thất bại.
        """
        try:
            # Đọc file JSON hiện tại
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Điều hướng đến vị trí cần cập nhật
            element = data
            for key in path[:-1]:
                element = element[key]

            # Tạo giá trị ngẫu nhiên mới
            new_value = DataGenerator.generate_random_data(data_type)
            element[path[-1]] = new_value

            # Ghi lại dữ liệu mới vào file JSON
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            return True, None  # Trả về True nếu cập nhật thành công và không có lỗi
        except Exception as e:
            error_message = f"Failed to update JSON at path: {path}. Error: {str(e)}"
            return False, error_message  # Trả về False nếu có lỗi xảy ra và thông báo lỗi


class XMLFileHandler:
    def __init__(self, file_path=None):
        # Sử dụng đường dẫn mặc định nếu không có file_path
        self.file_path = file_path or Paths().get_path_project()

    def read_xml(self):
        if os.path.exists(self.file_path):
            tree = elementTree.parse(self.file_path)
            return tree.getroot()
        else:
            raise FileNotFoundError(f"File '{self.file_path}' does not exist.")

    def _add_parameter(self, root, key, value):
        parameter = elementTree.Element('parameter')
        key_element = elementTree.SubElement(parameter, 'key')
        key_element.text = key
        value_element = elementTree.SubElement(parameter, 'value')
        value_element.text = str(value)
        root.append(parameter)

    def _write_tree(self, root):
        xml_str = elementTree.tostring(root, encoding='utf-8')
        pretty_xml = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="  ")

        # Loại bỏ dòng trống không cần thiết
        lines = pretty_xml.splitlines()
        cleaned_lines = [line for line in lines if line.strip()]

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(cleaned_lines))

    def add_element(self, key, value):
        root = self.read_xml()
        self._add_parameter(root, key, value)  # Sử dụng hàm _add_parameter
        self._write_tree(root)
        print(f"Thêm phần tử thành công: <parameter><key>{key}</key><value>{value}</value></parameter>")

    def generate_default_xml(self, json_data):
        root = elementTree.Element('environment')

        # Tạo các thẻ parameter từ json_data
        for key, value in json_data.items():
            self._add_parameter(root, key, value)

        # Ghi ra file XML với định dạng đẹp
        self._write_tree(root)
        print("Tạo file XML thành công từ JSON.")

    def remove_element(self, key, all=False):
        root = self.read_xml()
        removed_count = 0

        if all:
            # Xóa tất cả các phần tử có key trùng
            for element in root.findall('parameter'):
                key_element = element.find('key')
                if key_element is not None and key_element.text == key:
                    root.remove(element)
                    removed_count += 1
        else:
            # Chỉ xóa phần tử đầu tiên
            for element in root.findall('parameter'):
                key_element = element.find('key')
                if key_element is not None and key_element.text == key:
                    root.remove(element)
                    removed_count += 1
                    break  # Dừng lại sau khi xóa phần tử đầu tiên

        self._write_tree(root)
        if removed_count > 0:
            print(f"Đã xóa {removed_count} phần tử với key: '{key}'.")
        else:
            print(f"Không tìm thấy phần tử nào với key: '{key}' để xóa.")

    def edit_element(self, key, new_value, all=False):
        root = self.read_xml()
        updated_count = 0

        if all:
            # Cập nhật tất cả các phần tử có key trùng
            for element in root.findall('parameter'):
                key_element = element.find('key')
                if key_element is not None and key_element.text == key:
                    value_element = element.find('value')
                    if value_element is not None:
                        value_element.text = str(new_value)
                        updated_count += 1
        else:
            # Chỉ cập nhật phần tử đầu tiên
            for element in root.findall('parameter'):
                key_element = element.find('key')
                if key_element is not None and key_element.text == key:
                    value_element = element.find('value')
                    if value_element is not None:
                        value_element.text = str(new_value)
                        updated_count += 1
                    break  # Dừng lại sau khi cập nhật phần tử đầu tiên

        self._write_tree(root)
        if updated_count > 0:
            print(f"Đã cập nhật {updated_count} phần tử với key: '{key}' thành giá trị mới.")
        else:
            print(f"Không tìm thấy phần tử nào với key: '{key}' để cập nhật.")


def read_section_from_md(file_path, index):
    """
    Đọc file .md và lấy tiêu đề bắt đầu bằng # theo thứ tự chỉ định.

    Args:
        file_path (str): Đường dẫn đến file .md cần đọc.
        index (int): Vị trí của tiêu đề (bắt đầu bằng dấu #) cần lấy ra.

    Returns:
        str: Tiêu đề thứ 'index' bắt đầu bằng dấu # trong file.

    Raises:
        ValueError: Nếu 'index' không phải là số nguyên dương.
        FileNotFoundError: Nếu đường dẫn file không hợp lệ.
    """
    if not isinstance(index, int) or index <= 0:
        raise ValueError("Index phải là số nguyên dương.")

    count = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#'):
                count += 1
                if count == index:
                    return line.lstrip('#').strip()
    return None  # Nếu không tìm thấy tiêu đề ở vị trí chỉ định


# # # JSON data cần truyền vào hàm
# json_data = {
#     "Identity url": "https://accounts.vbd.vn",
#     "App url": "http://172.17.1.18:30609",
#     "Tenant url": "https://c4i2-v6.vbd.vn/",
#     "Vdms version": "vdms.api: 6.1.4.25 - vietbando.search: 9.0.8",
#     "Vdms version detection time": "2024-09-24 14:15:02",
#     "Python project": "[3.3.0] last update: 24/09/2024 - 15:00 PM"
# }
#
# path_project = Paths().get_path_project()
# path_file_xml = os.path.join(path_project, "configAllure", "thanhtest123.xml")
#
# # Tạo đối tượng xử lý XML
# handler = XMLFileHandler(path_file_xml)
# handler.edit_element("Phiên bản 222", "Đạp chai")
# handler.edit_element("Thời gian build", "Đạp chai222")
#
# # Gọi hàm để sinh XML từ JSON
# handler.generate_default_xml(json_data)
# handler.add_element('New parameter', 'New value')
# handler.remove_element("New parameter", True)