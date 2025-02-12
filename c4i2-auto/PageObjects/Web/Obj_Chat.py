class Obj_Chat:
    iconKenhLienLac = ('//img[@alt="{0}"]').format("Kênh liên lạc")
    txtTimKenh = '//div[contains(text(), "Tìm kênh")]'
    txtTimKiemKenh = '//input[contains(@class, "search-box-control")]'
    optionFirst = '//div[contains(@class, "result-item can-hover")][1]'
    textareaChat = '//textarea[contains(@class, "chat")]'

    # new
    iconAdd = ('(//i[contains(@class, "{0}")])').format("fal fa-plus")
    optionTaoKenh = ('(//*[text()="{0}"])[1]').format("Tạo kênh")
    chanelTypePublic = ('//div[contains(@class, "channel-switch-type")][.//span[text()="{0}"]]').format(
        "Kênh công khai")
    chanelTypePrivate = ('//div[contains(@class, "channel-switch-type")][.//span[text()="{0}"]]').format(
        "Kênh riêng tư")
    btnTaoKenh = ('//button[.//span[text()="{0}"]]').format("Tạo Kênh")

    # addmember
    iconDetail = ('(//i[contains(@class, "{0}")])').format("fas fa-info")
    btnAddMember = ('//button[.//span[text()="{0}"]]').format("Thêm")
    inputSeachMember = ('//input[@placeholder="{0}"]').format("Tìm người dùng")
    btnXacNhan = ('//button[.//span[text()="{0}"]]').format("Xác Nhận")

    # deletemember
    btnQuanLy = ('//button[.//span[text()="{0}"]]').format("Quản lý")

    # deletechanel
    iconChevronDown = ('(//i[contains(@class, "{0}")])').format("fas fa-chevron-down")
    btnXacNhanXoaKenh = '//span[contains(text(), "Xác nhận")]'
