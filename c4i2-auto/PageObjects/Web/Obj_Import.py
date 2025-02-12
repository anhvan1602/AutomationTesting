class Obj_Import:
    btnChonTapTin = ('//span[text()="Chọn tập tin"]')
    btnChonThuMuc = ('//span[text()="Chọn thư mục"]')
    btnChonFile = ('//span[text()="Chọn file"]')
    btnBatDauImport = ('//span[text()="Bắt đầu"]')
    optionFirst = ('(//div[contains(@class, "list-item-subtitle")])[1]')

    btnXacNhanXoa = '//span[contains(text(), "Xác nhận")]'
    iconClosePopup = '//div[contains(@class,"popup-header")]//child::i[contains(@class, "fal fa-times")]'


class ObjImportFunction:
    @staticmethod
    def icon_delete_file_import(label):
        return f'(//div[contains(text(), "{label}")]//ancestor::div[contains(@class, "list-item-container")]//child::i[contains(@class, "fa-trash-alt")])[1]'

    @staticmethod
    def icon_in_file(label, icon):
        return f'//div[text()="{label}"]//ancestor::div[contains(@class, "list-item")]//child::button//i[contains(@class, "{icon}")]'
