class AppConfig:
    # Navigate
    menuLink_LayerManager = '//a[@href="/ndms2/app-config/layer-manager"]'

    # LayerManager
    btnAddNewLayer = '//button[contains(@class,"btn--success") and //i[@class="fal fa-plus  "]]'
    btnSubmitCreateNewLayer = '//div[@class="new-layer-form"]//span[text()="Create"]'
    txtSearchLayer = '(//input[@placeholder="Enter keyword to search"])[1]'
    txtSearchAttributeLayer = '(//input[@placeholder="Enter keyword to search"])[2]'

    # Contral list item Layer
    bntMenuControlByLayerName = '(//div[contains(@class,"layer-item") and .//div[@class="list-item-title ml-ellipsis" and text()="{}"]])[1]//button'
    btnRename = '//button[.//span[text()="Rename"]]'
    btnDuplication = '//button[.//span[text()="Duplicate"]]'
    btnClear = '//button[.//span[text()="Clear"]]'
    txtLayerItem = '(//div[@class="layer-item active "])[1]//input'
    txtLayerItem_success = '//button[contains(@class,"btn--success")]//i[contains(@class,"fas fa-check")]'
    txtLayerItem_cancel = '(//div[@class="layer-item-actions"])[1]//button[contains(@class,"btn--danger")]'

    btnDuplicateSubmit = '//button[.//span[text()="Duplicate"]]'
    btnDuplicateCancel = '//button[.//span[text()="Cancel"]]'
    txtDuplicateLayerName = '//div[contains(@class,"form-label") and ./div[text()="Layer name"]]/..//input'

    # Notify
    isSuccess = '//div[@class, "toast toast-success"]'

    menuHome_ChooseConfig = '//button[@title="Application info"]'
    menuHome_ChooseConfig_AppConfig = '//div[@role="menuitem" and .//div[text()="App configuration"]]'
