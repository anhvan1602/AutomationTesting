class Obj_SuKien:
    iconSuKien = ('//img[@alt="{0}"]').format("Sự kiện")
    txtCachDay = '//span[contains(text(),"Cách đây")]//ancestor::div[contains(@class, "justify-between")]//child::div[contains(@class, "dropdown-btn-text")]'
    btnMoRongGrid = '//i[contains(@class, "fal fa-list")]'
    btnTimKiem = ('//button[.//span[text()="{0}"]]').format("Tìm kiếm")