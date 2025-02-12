class Obj_TongHop:
    iconNhanDangTongHop = ('//img[@alt="{0}"]').format("Nhận dạng tổng hợp")
    tabThuVien = ('//button[contains(.,"{0}")]').format("Thư viện")
    tabNhapLieu = ('//button[contains(.,"{0}")]').format("Nhập liệu")
    tabPhatHien = ('//button[contains(.,"{0}")]').format("Phát hiện")
    # new
    btnThemMoiGuongMat = ('//span[text()="{0}"]').format("Thêm mới")
    btnLuuThemMoi = '//div[contains(@class,"window-manager__popup")]//button[.//span[text()="Thêm mới"]]'

    # edit
    txtSearchGuongMat = ('//input[@placeholder="{0}"]').format("Nhập họ và tên")
    btnTimKiem = ('//button[.//span[text()="{0}"]]').format("Tìm kiếm")
    iconEdit = '(//i[contains(@class,"fal fa-edit")])[1]'
    btnCapNhatFace = ('//button[.//span[text()="{0}"]]').format("Cập nhật")

    # delete
    checkboxFace = '(//label[@class = "checkbox-item"])[2]'
    btnDelete = '//span[contains(text(), "Xóa những mục đã chọn (1)")]'
    btnXacNhan = '//span[contains(text(), "Xác nhận")]'

    # tab Phát hiện - search
    txtSearchName = ('//input[@placeholder="{0}"]').format("Họ và tên")
    txtCachDay = '//span[contains(text(),"Cách đây")]//ancestor::div[contains(@class, "justify-between")]//child::div[contains(@class, "dropdown-btn-text")]'
    btnReset = ('//button[.//span[text()="{0}"]]').format("Đặt lại")

    # tab Thư viện - search
    txtSearchID = ('//input[@placeholder="{0}"]').format("Nhập CCCD/CMND/Hộ chiếu")
    btnResetLibrary = ('//button[.//span[text()="{0}"]]').format("Xóa")
