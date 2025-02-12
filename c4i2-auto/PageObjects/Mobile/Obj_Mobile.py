class Obj_Function:
    @staticmethod
    def TextView(label):
        return f'//android.widget.TextView[@text="{label}"]'

    @staticmethod
    def ContainsTextView(label):
        return f'//android.widget.TextView[contains(@text, "{label}")]'

    @staticmethod
    def Button(label):
        return f'//android.widget.Button[@text="{label}"]'

    @staticmethod
    def EditText(label):
        return f'//android.widget.EditText[@text="{label}"]'


