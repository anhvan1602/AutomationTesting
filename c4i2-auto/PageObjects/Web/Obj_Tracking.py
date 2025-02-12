class Obj_Tracking:
    iconGiamSatHanhTrinh = ('//img[@alt="{0}"]').format("Giám sát hành trình")
    iconFilterStatus = '//i[contains(@class, "fal fa-filter")]'


class ObjTrackingFuntion:
    @staticmethod
    def button_tracking(label):
        return f'//button[contains(@class, "tracking-tracker")]//child::div[contains(text(), "{label}")]'

    @staticmethod
    def checkbox_filter(label):
        return f'//div[contains(text(), "{label}")]//ancestor::div[contains(@class, "flex-grow")]//span[contains(@class, "checkbox--icon")]'

    @staticmethod
    def icon_signal(label):
        return f'//i[contains(@style, "{label}")]'
