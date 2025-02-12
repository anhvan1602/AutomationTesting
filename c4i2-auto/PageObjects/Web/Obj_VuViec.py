class Obj_VuViec:
    btnTaoVuViec = ('//span[text()="{0}"]').format("Tạo vụ việc")
    iconVuViec = ('//img[@alt="{0}"]').format("Vụ việc")
    txtSoDoiTuong = ('//div[contains(@class, "form-control-label") and .//div[text()="{0}"]]//input').format(
        "Số đối tượng")
    txtSoPhuongTien = ('//div[contains(@class, "form-control-label") and .//div[text()="{0}"]]//input').format(
        "Số lượng xe")
    txtSoNanNhan = ('//div[contains(@class, "form-control-label") and .//div[text()="{0}"]]//input').format(
        "Số nạn nhân")
    btnDanhSachDoiTuong = ('//div[contains(@class, "form-control-label") and .//div[text()="{0}"]]//button').format(
        "Đối tượng")
    btnDanhSachPhuongTien = ('//div[contains(@class, "form-control-label") and .//div[text()="{0}"]]//button').format(
        "Biển số xe")
    btnDanhSachNanNan = ('//div[contains(@class, "form-control-label") and .//div[text()="{0}"]]//button').format(
        "Nạn nhân")
    btnEditDoiTuong = (
        '//div[@class="popup-header" and .//h3[text()="Đối tượng"]]/..//div[contains(@class,"section-header flex")  and .//h3[text()="{0}"]]//button[.//i[contains(@class,"fal fa-pencil")]]').format(
        "Đối tượng 1")
    btnTraCuuNhanDangDoiTuong = ('//button[.//span[text()="{0}"]]').format("Tra cứu nhận dạng")
    btnTraCuuLichSuNhanDang = ('//button[.//span[text()="{0}"]]').format("Lịch sử nhận dạng")
    btnCapNhatDoiTuong = ('//button[.//span[text()="{0}"]]').format("Cập nhật đối tượng")
    btnChonDoiTuongDauTien = (
        '(//div[contains(@class,"popup-container") and .//h3[text()="Nhận dạng đối tượng"]]//div[contains(@class,"dg-row selectable-row")])[1]//button[.//span[text()="{0}"]]').format(
        "Chọn")
    btnLuuDoiTuong = ('//span[contains(text(),"Lưu")]')
    btnLuuPhuongTien = ('//button//span[text()="{0}"]').format("Lưu")
    btnSearchPhuongTien = '//i[contains(@class, "fal fa-file-search")]'
    resultSearchPhuongTien = '(//span[contains(@class, "auto-number")])[1]'
    btnThemInPopup = ('(//span[contains(text(),"Thêm")])[last()]')
    btnLuuNanNhan = ('//button//span[text()="{0}"]').format("Lưu")
    txtSearchVuViec = ('//input[@placeholder="{0}"]').format("Nhập từ khóa")
    btnEditVuviecGrid = '(//div[contains(@class,"selectable-row")])[1]//button[.//i[contains(@class,"fal fa-edit")]]'
    btnCapNhatVuViec = ('//button[.//span[text()="{0}"]]').format(("Cập nhật vụ việc"))
    btnTimKiem = ('//button[.//span[text()="{0}"]]').format("Tìm kiếm")
    btnTiepTuc = '//button[.//span[text()="Tiếp tục"]]'
    btnSubmitVuViec = '//div[contains(@class,"window-manager__popup")]//button[.//span[text()="Tạo vụ việc"]]'
    txtvideo = '//input[@accept="video/*"]/..'
    tabVuViec = ('(//span[contains(text(), "{0}")])[last()]').format("Vụ việc")
    # Import
    tabThuVien = ('(//span[contains(text(), "{0}")])[last()]').format("Đối tượng")
    tabNhapLieu = ('(//span[contains(text(), "{0}")])[last()]').format("Nhập liệu")
    # Delete
    checkboxVuViec = '(//span[contains(@class, "checkbox-input")])[4]'

    btnDelete = '//span[contains(text(), "Xóa vụ việc")]'
    btnXacNhan = '(//span[contains(text(), "Xóa")])[2]'
    btnHuy = '//span[contains(text(), "Hủy")]'

    # Search
    btnReset = ('//button[.//span[text()="{0}"]]').format("Đặt lại")
    btnMoRongGrid = '//i[contains(@class, "fal fa-list")]'

    # tab Đối tượng
    btnTaoDoiTuong = ('//span[text()="{0}"]').format("Tạo đối tượng")
    btnSubmitDoiTuong =('//div[contains(@class,"window-manager__popup")]//button[.//span[text()="{0}"]]').format("Tạo đối tượng")
    btnUpdateDoiTuong = ('//div[contains(@class,"window-manager__popup")]//button[.//span[text()="{0}"]]').format(
        "Cập nhật đối tượng")
    btnDeleteDoiTuong = ('//span[contains(text(), "{0}")]').format("Xóa đối tượng")
    iconEditDoiTuong = '(//i[contains(@class,"fal fa-edit")])[1]'
    elementLastPopup = '//div[text()="Ghi chú"]'

    xpathIDCase = '//div[contains(@cellid, "CaseID")]//child::div[contains(@class, "long-text")]'
    xpathElementInGrid = '//div[@cellid]'

