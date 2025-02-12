class Default:
    # # # Staging # # #
    url = "https://c4i2-v6.vbd.vn/"
    version = "1.22.0"
    projectname = "c4i2 - Trung tâm chỉ huy Công an thành phố"
    username = "qc_van_1"
    password = "123123123"
    timeOut = 15

    # Account Chat
    username_from = "qc_van_1"
    password_from = "123123123"
    username_to = "qc_van_2"
    password_to = "123123123"

    # Account Permission
    username_permission = "qc_van_1"
    password_permission = "123123123"
    username_check_permission = "qc_van_2"
    password_check_permission = "123123123"

    # Web Language
    defaultLanguage = 'Tiếng Việt'
    # defaultLanguage = 'English'

    # --window-size
    windowSize = "1920,1080"

    # Headless Brower
    headlessBrowser = False

    # Split Screen (TSC Permission)
    useSplitScreen = False

    # Number Reload
    numberReload = 1

    # EventSimulator
    rabbit_url = "http://172.17.1.4:15672/api/exchanges/%2F/amq.default/publish"
    routing_key = "vdfs_vig_lpr_staging_v6"
    cookies = "m=2258:dmJkOnZiZA%253D%253D"


class Import:
    # Tên cột trạng thái Import
    NameColumnStatus = "Status Import"
    # Các trạng thái Import
    Imported = "Imported"
    IncompleteImport = "Incomplete Import"
    NotImported = "Not Imported"
