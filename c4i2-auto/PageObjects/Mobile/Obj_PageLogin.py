class Obj_PageLogin:
    # Cấp quyền cho ứng dung
    btnAllow = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
    iconBack = '//android.widget.ImageButton[@content-desc="Back"]'
    # Thay đổi kết nối ứng dụng
    changeAuthority = '(//android.widget.EditText)[2]'
    changeDomain = '(//android.widget.EditText)[3]'

    # Page Login
    txtUsername = '//android.widget.EditText[@text="Tên đăng nhập"]'
    txtPassword = '//android.widget.EditText[@text="Mật khẩu"]'
    btnLogin = '//android.widget.TextView[@text="Đăng nhập"]'