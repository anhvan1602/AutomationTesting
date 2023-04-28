class Obj_PageThietLapHeThong:
    tabVaiTro = '//span[contains(text(),"Vai trò")]'
    btnPhanQuyen = '//div[contains(@class,"dg-row") and .//div[text()="qah_test"]]//*[contains(@class,"fal fa-user-tag")]'
    # Quyền chức năng
    iconDropDown = '//div[contains(@class,"tree-header") and .//*[text()="TÀI NGUYÊN VÀ TÍNH NĂNG"]]//*[contains(@class,"fal fa-angle")]'

    btnSwitchToogle = '//div[contains(@class,"tree-header") and .//div[text()="Xem"]]//div[contains(@class,"switch-toogle")]'

    btnDongToanBo = '//span[contains(text(),"Đóng toàn bộ")]'