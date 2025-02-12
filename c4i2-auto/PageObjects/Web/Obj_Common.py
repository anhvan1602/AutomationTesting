class ObjCommon:
    @staticmethod
    def search_textbox(label):
        return f'//div[contains(text(), "{label}")]//ancestor::div[contains(@class, "form-control-label")]//child::input'

    @staticmethod
    def input_search(label):
        return f'//input[@placeholder="{label}"]'

    @staticmethod
    def input_search_number(label):
        return f'//div[contains(text(),"{label}")]//ancestor::div[contains(@class, "form-control")]//child::input[@type="number"]'

    @staticmethod
    def element_text(label):
        return f'(//*[text()="{label}"])[1]'

    @staticmethod
    def edit_icon(label):
        return f'//div[contains(text(), "{label}")]//ancestor::div[contains(@class, "dg-row")]//child::i[contains(@class,"fal fa-edit")]'

    @staticmethod
    def dropdown_list(label):
        return f'(//div[contains(@class,"form-control-label") and .//div[text()="{label}"]]//div[contains(@class,"as-control-container")])[last()]'

    @staticmethod
    def label_dropdown_list(label):
        return f'//div[contains(@class,"form-control-label") and .//div[text()="{label}"]]//div[contains(@class,"as-control-container")]'

    @staticmethod
    def radio_button(label):
        return f'//div[@class="checkbox-form" and .//span[contains(text(), "{label}")]]//child::span[contains(@class, "radio-input")]'

    @staticmethod
    def checkbox_button(label):
        return f'//*[contains(text(), "{label}")]/preceding::span[contains(@class, "checkbox")][1]'

    @staticmethod
    def txt_search_time(label):
        return f'//div[contains(text(),"{label}")]//ancestor::div[contains(@class, "form-control")]//child::div[contains(@class, "form-control flex")]'

    @staticmethod
    def txt_search_time_group(group_name, label):
        return f'//div[contains(@class,"section-panel") and .//*[text()="{group_name}"]]//*[text()="{label}"]'

    @staticmethod
    def input_search_by_group(group_name, label):
        return f'//div[contains(@class,"section-panel") and .//*[text()="{group_name}"]]//*[text()="{label}"]/../..//input'


    @staticmethod
    def input_search_time(label):
        return f'//div[contains(text(),"{label}")]//ancestor::div[contains(@class, "form-control")]//child::input[contains(@class, "input-text")]'

    @staticmethod
    def option_time_stamp(label):
        return f'//div[contains(@class,"as-dropdown-item-button") and contains(text(), "{label}")]'

    @staticmethod
    def toggle_switch(label):
        return f'//div[contains(@class,"form-control-label") and .//div[text()="{label}"]]//div[contains(@class,"switch-toogle")]'

    @staticmethod
    def toggle_checkbox(label):
        return f'//div[contains(@class,"form-control-label") and .//div[text()="{label}"]]//span[contains(@class,"checkbox-input")]'

    @staticmethod
    def item_checkbox(label):
        return f'(//div[text()="{label}"]//ancestor::div[contains(@class, "dg-row")]//child::label[contains(@class, "checkbox")])[1]'

    @staticmethod
    def item_collapsible(label):
        return f'//div[contains(@class, "collapsible-item")]//child::div[contains(text(), "{label}")]'

    @staticmethod
    def text_span(label):
        return f'//span[text()="{label}"]'

    @staticmethod
    def result_item(label):
        return f'(//div[contains(@class, "result-item")]//child::span[contains(text(), "{label}")])[1]'

    @staticmethod
    def ellipsis_icon(label):
        return f'(//*[contains(text(), "{label}")]//ancestor::div[contains(@class, "item")]//child::*[contains(@class,"fa-ellipsis")])[last()]'

    @staticmethod
    def option_menu(label):
        return f'(//div[contains(@class, "menu")][.//*[text()="{label}"]])[last()]'

    @staticmethod
    def item_last_in_list(label):
        return f'(//div[contains(@class, "list-item")]//child::*[contains(text(), "{label}")])[last()]'

    @staticmethod
    def checkbox_filter(label):
        return f'(//div[contains(text(), "{label}")]//ancestor::div[contains(@class, "flex-grow")]//span[contains(@class, "checkbox--icon")])[1]'

    @staticmethod
    def switcher_button(label):
        return f'//*[contains(text(), "{label}")]/ancestor::div[contains(@class, "switcher-popup-item")][1]'

    @staticmethod
    def action_button(label, action):
        return f'//div[text()="{label}"]//ancestor::div[contains(@class, "dg-row")]//child::button//i[contains(@class, "{action}")]'

    @staticmethod
    def button_with_icon(label):
        return f'(//i[contains(@class, "{label}")])[1]'

    @staticmethod
    def button_with_text(label):
        return f'(//button//span[contains(text(), "{label}")])[1]'