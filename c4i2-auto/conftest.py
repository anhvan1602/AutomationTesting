import allure
import pytest
import json
import os
from allure_commons.types import AttachmentType


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    It checks if the browser is a Selenium WebDriver object or a tuple
    containing Selenium WebDriver objects, and handles both cases accordingly
    :param item:
    :param call:
    :return: Capture and attach a screenshot to the Allure report when a test case fails.
    """
    outcome = yield
    rep = outcome.get_result()

    # Kiểm tra nếu testcase thất bại và đang ở giai đoạn 'call'
    if rep.when == "call" and rep.failed:
        try:
            # Kiểm tra xem browser là một đối tượng Selenium hay một tuple chứa các đối tượng Selenium
            if hasattr(item.funcargs["browser"], "get_screenshot_as_png"):
                # Nếu chỉ có một trình duyệt
                allure.attach(item.funcargs["browser"].get_screenshot_as_png(), name="screenshot_failed",
                              attachment_type=AttachmentType.PNG)
            else:
                # Nếu có hai trình duyệt, lặp qua từng trình duyệt trong tuple và đính kèm ảnh chụp màn hình
                for browser in item.funcargs["browser"]:
                    allure.attach(browser.get_screenshot_as_png(), name="screenshot_failed",
                                  attachment_type=AttachmentType.PNG)
        except Exception as e:
            print("Không thể thêm screenshot vào allure report:", e)


def capture_screenshot_and_attach_allure(driver, name="Screenshot"):
    """
    Chụp màn hình và đính kèm vào báo cáo Allure.

    :param driver: Đối tượng WebDriver của Selenium.
    :param name: Tên tệp đính kèm (mặc định là "Screenshot").
    """
    allure.attach(driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)


def attach_table_to_allure(data, name="Data Test"):
    """
    Attach a table containing the provided data to Allure report.

    Parameters:
    - data (list of dicts): List of dictionaries containing data to be displayed in the table.

    Returns:
    None
    """
    import pandas as pd
    df = pd.DataFrame(data)
    html_table = df.to_html(index=False, justify='left', classes="table table-bordered table-hover")

    with allure.step(f"{name}"):
        allure.attach(html_table, "Table", allure.attachment_type.HTML)


@pytest.fixture
def mask_parameters(request):
    """Fixture to mask parameters in Allure report for each test."""
    if hasattr(request.node, 'callspec'):
        param_names = request.node.callspec.params.keys()
        param_values = request.node.callspec.params.values()

        for name, value in zip(param_names, param_values):
            allure.dynamic.parameter(name=name, value="****", mode=allure.parameter_mode.MASKED)


def load_skip_config():
    """
        Load skip configuration from a JSON file.

        Returns:
            dict: Dictionary containing skip configuration.
        """
    config_file = os.getenv('SKIP_CONFIG_FILE', 'skip_tests.json')
    project_root = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(project_root, config_file)
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


skip_config = load_skip_config()


def pytest_collection_modifyitems(config, items):
    """
    Modify the collected test items to apply skip markers based on the skip configuration.
    The test case identifier format is ClassName::TestCaseName.
    Args:
        config (Config): Pytest configuration object.
        items (list): List of collected test items.
    """
    skip_tests = skip_config.get('skip_tests', {})

    for item in items:
        # Construct identifier in the format 'ClassName::TestCaseName'
        identifier_case = f"{item.parent.name}::{item.name.split('[')[0]}"
        identifier_class = f"{item.parent.name}"

        # Check if the test case or class should be skipped based on the configuration
        for identifier in [identifier_case, identifier_class]:
            if identifier in skip_tests:
                test_info = skip_tests[identifier]
                reason = test_info['reason']
                skip_marker = pytest.mark.skip(reason=reason)
                item.add_marker(skip_marker)

                issue = test_info.get('issue')
                if issue:
                    issue_marker = allure.issue(issue, issue)
                    item.add_marker(issue_marker)
                break  # Stop checking further if skip marker applied
