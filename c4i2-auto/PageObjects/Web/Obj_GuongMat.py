class Obj_GuongMat:
    iconNhanDangGuongMat = ('//img[@alt="{0}"]').format("Nhận dạng gương mặt")
    iconNhanDangGuongMat_navigation = "//i[contains(@class, 'fa-user-friends')]"
    tabThuVien = ('(//span[contains(text(), "{0}")])[last()]').format("Thư viện")
    tabNhapLieu = ('(//span[contains(text(), "{0}")])[last()]').format("Nhập liệu")
    tabPhatHien = ('(//span[contains(text(), "{0}")])[last()]').format("Phát hiện")
    tabCauHinh = ('(//span[contains(text(), "{0}")])[last()]').format("Cấu hình")

    # new
    btnThemMoiGuongMat = ('//span[text()="{0}"]').format("Thêm mới")
    btnLuuThemMoi = '//div[contains(@class,"window-manager__popup")]//button[.//span[text()="Thêm mới"]]'

    # edit
    txtSearchGuongMat = ('//input[@placeholder="{0}"]').format("Nhập họ và tên")
    btnTimKiem = ('//button[.//span[text()="{0}"]]').format("Tìm kiếm")
    iconEdit = '(//i[contains(@class,"fal fa-edit")])[1]'
    btnCapNhatFace = ('(//button[.//span[text()="{0}"]])[last()]').format("Cập nhật")
    btnDateNow = '//span[contains(text(), "Hôm nay")]'

    # delete
    checkboxFace = '(//label[contains(@class, "checkbox-item")])[2]'
    btnDelete = '//span[contains(text(), "Xóa những mục đã chọn (1)")]'
    btnXacNhan = '//span[contains(text(), "Xác nhận")]'

    # tab Phát hiện - search
    txtSearchName = ('//input[@placeholder="{0}"]').format("Họ và tên")
    txtCachDay = '//span[contains(text(),"Cách đây")]//ancestor::div[contains(@class, "justify-between")]//child::div[contains(@class, "dropdown-btn-text")]'
    btnReset = ('//button[.//span[text()="{0}"]]').format("Đặt lại")
    btnMoRongGrid = '//i[contains(@class, "fal fa-list")]'

    # tab Thư viện - search
    txtSearchNameLib = ('//input[@placeholder="{0}"]').format("Nhập họ và tên")
    txtSearchID = ('//input[@placeholder="{0}"]').format("Nhập CCCD/CMND/Hộ chiếu")
    btnResetLibrary = ('//button[.//span[text()="{0}"]]').format("Xóa")

    # tab Cấu hình
    btnThemMoiLTD = ('//span[text()="{0}" and @class="btn__text"]').format("Thêm")
    btnLuuLTD = '(//button[.//span[text()="Thêm"]])[last()]'
    btnXacNhanXoa = '(//span[contains(text(), "Xác nhận")])[last()]'

    # others
    iconDetail = '(//i[contains(@class, "fas fa-info")])[1]'
    btnLichSu = ('//button[.//span[text()="{0}"]]').format("Lịch sử nhận dạng")
    btnThemTheoDoi = ('//button[.//span[text()="{0}"]]').format("Thêm theo dõi")
    iconDeleteTracking = '(//i[contains(@class, "fal fa-trash")])[last()]'
    btnCapNhatDanhSachMienTru = ('//button[.//span[text()="{0}"]]').format("Cập nhật danh sách miễn trừ")
    elementScrollDown = '//div[text()="Diễn biến"]'
    inputDateInPopUp = '//div[contains(@class,"form-control-label") and .//div[text()="{0}"]]//div[contains(@class,"dtp-control-container")]'.format(
        "Ngày bắt đầu")


class ObjGuongmatFuntion:

    @staticmethod
    def icon_delete_tracking(label):
        return f'//span[text()="{label}"]//ancestor::div[contains(@class, "vui-card")]//child::i[contains(@class, "fal fa-trash")]'
