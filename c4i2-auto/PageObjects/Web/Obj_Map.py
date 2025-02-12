class Obj_Map:
    iconKhaiThacBanDo = ('//img[@alt="{0}"]').format("Khai thác bản đồ")
    iconTimViTri = ('(//i[contains(@class,"{0}")])').format("fal fa-search")
    optionViTriCuaBan = ('(//div[contains(text(),"{0}")])').format("Vị trí của bạn")
    popupViTriHienTai = '(//div[contains(@class,"marker-popup")])'
    iconClosePopupViTriHienTai = '//div[contains(@class,"marker-popup")]//child::i[contains(@class, "fal fa-times")]'
    iconMoRongAnh = '(//div[contains(@class,"marker-popup")])//child::i[contains(@class, "fal fa-expand")]'
    imageInPopup = '//div[contains(@class, "marker-popup")]//child::img'
    inputSearchLocation = '//input[contains(@class, "search-input")]'
    suggestOne = '(//div[contains(@class,"suggest-hint")])[1]'

    iconTimDuong = ('(//i[contains(@class,"{0}")])').format("fal fa-route")
    tabLoTrinh = ('(//span[contains(text(),"{0}")])').format("Lộ trình")
    xpath_route = '//div[contains(@class,"guide")]//child::span'

    xpathMap = ('//canvas[contains(@class, "maplibregl-canvas")]')

    # Bản đồ tác chiến #
    iconBanDoTacChien = ('(//i[contains(@class,"{0}")])').format("fal fa-tools")
    itemRename = '(//div[@class="list-item-title"])//child::input'
    btnApDung = ('//button[.//span[text()="{0}"]]').format("Áp dụng")

    # Nhãn
    iconNhan = ('(//div[@class="tgb-group"]//child::button)[2]')
    verifyIconNhan = ('(//div[@class="tgb-group"]//child::button)[2]//child::*[@fill="rgb(69, 148, 239)"]')

    # Điểm
    iconDiem = ('(//div[@class="tgb-group"]//child::button)[3]')
    verifyIconDiem = ('(//div[@class="tgb-group"]//child::button)[3]//child::*[@fill="rgb(69, 148, 239)"]')

    # Đường
    iconDuong = ('(//div[@class="tgb-group"]//child::button)[4]')
    verifyIconDuong = ('(//div[@class="tgb-group"]//child::button)[4]//child::*[@fill="rgb(69, 148, 239)"]')

    # Vùng
    iconVung = ('(//div[@class="tgb-group"]//child::button)[5]')
    verifyIconVung = ('(//div[@class="tgb-group"]//child::button)[5]//child::*[@fill="rgb(69, 148, 239)"]')

    # Tìm kiếm nâng cao
    inputLopDuLieu = '//div[contains(text(), "Lớp dữ liệu")]//ancestor::div[contains(@class, "form-control-label")]//child::input[@placeholder="Nhập từ khóa để tìm kiếm"]'
    verifyResultsSearch = '//div[contains(@class, "load-list")]'
    iconDelete = '//i[contains(@class, "fal fa-trash")]'

    # Tài nguyên và tính năng #
    iconTaiNguyenVaTinhNanng = ('(//i[contains(@class,"{0}")])').format("fal fa-layer-group")
    markerVideo = "//i[contains(@class, 'fad fa-video')]//ancestor::span[not(contains(@style, 'transform: rotate(0deg)'))]"

    # Loại bản đồ #
    iconLoaiBanDo = ('(//i[contains(@class,"{0}")])').format("fal fa-send-backward")

