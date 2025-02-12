class Obj_BienSo:
    iconNhanDangBienSo = ('//img[@alt="{0}"]').format("Nhận dạng biển số xe")
    tabThuVien = ('(//span[contains(text(), "{0}")])[last()]').format("Thư viện")
    tabNhapLieu = ('(//span[contains(text(), "{0}")])[last()]').format("Nhập liệu")
    tabPhatHien = ('(//span[contains(text(), "{0}")])[last()]').format("Phát hiện")
    tabCauHinh = ('(//span[contains(text(), "{0}")])[last()]').format("Cấu hình")

    # new
    btnThemMoiBSX = ('//span[text()="{0}" and @class="btn__text"]').format("Thêm")
    btnLuuThemMoi = '(//button[.//span[text()="Thêm"]])[3]'
    iconClosePopup = '//button[contains(@class,"btn btn--default btn--round")]'

    # edit
    txtSearchBSX = ('//input[@placeholder="{0}"]').format("Nhập biển số xe")
    btnTimKiem = ('//button[.//span[text()="{0}"]]').format("Tìm kiếm")
    iconEdit = '(//i[contains(@class,"fal fa-edit")])[1]'
    btnCapNhatBSX = ('//button[.//span[text()="{0}"]]').format("Cập nhật")

    # delete
    checkboxBSX = '(//label[contains(@class,"checkbox-item")])[2]'
    btnDelete = '//span[contains(text(), "Xóa những mục đã chọn (1)")]'
    btnXacNhan = '//span[contains(text(), "Xác nhận")]'
    btnHuy = '//span[contains(text(), "Hủy")]'
    btnXacNhanXoa = '(//span[contains(text(), "Xóa")])[last()]'

    # search
    ddlBSX = '//div[contains(@class,"form-control-label") and .//div[text()="Chọn biển số"]]//i[contains(@class,"far fa-chevron")]'
    txtCachDay = '//span[contains(text(),"Cách đây")]//ancestor::div[contains(@class, "justify-between")]//child::div[contains(@class, "dropdown-btn-text")]'
    btnReset = ('//button[.//span[text()="{0}"]]').format("Đặt lại")

    # others
    iconDetail = '(//i[contains(@class, "fas fa-info")])[1]'
    btnLichSu = ('//button[.//span[text()="{0}"]]').format("Lịch sử")
    btnThemTheoDoi = ('//button[.//span[text()="{0}"]]').format("Thêm theo dõi")
    iconDeleteTracking = '//i[contains(@class, "fal fa-trash")]'
