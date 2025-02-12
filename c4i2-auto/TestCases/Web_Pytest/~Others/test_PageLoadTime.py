import time
from urllib.parse import urljoin

import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from WebApplications.PageLoadTime import PageLoadTime
from WebApplications.PageHome import LoginPage
from conftest import capture_screenshot_and_attach_allure
import parametrize_from_file as pff


def wait_for_worker():
    """
    The `wait_for_worker` function is designed to support parallel execution in testing environments.
    """
    import os
    worker_id = os.environ.get('PYTEST_XDIST_WORKER', 'gw0')
    if worker_id.startswith('gw'):
        worker_num = int(worker_id[2:])

        if worker_num > 0:
            delay_time = worker_num * 5
            print(f"Worker {worker_id} đang chờ {delay_time} giây...")
            time.sleep(delay_time)


@pytest.fixture(scope='class')
def browser():
    driver = get_chrome_driver()
    driver.implicitly_wait(Default.timeOut)
    # driver.maximize_window()

    default_tenant = Default()

    url = default_tenant.url
    username = default_tenant.username
    password = default_tenant.password

    page_login = LoginPage(driver)
    driver.get(url)
    wait_for_worker()
    page_login.do_login(username, password)
    time.sleep(1)

    yield driver
    driver.quit()


@pytest.fixture(scope='class', autouse=True)
def save_current_url(browser):
    driver = browser
    current_url = driver.current_url
    yield current_url


is_first_test = True


@pytest.fixture(scope='function', autouse=True)
def setup_url(browser, save_current_url):
    global is_first_test
    if not is_first_test and save_current_url is not None:
        driver = browser
        driver.get(save_current_url)
    is_first_test = False
    yield


pageBase = PageBase(browser)
pathDataTestLoadTime = pageBase.load_path_data_file_from_path("Datas_Others", "Test_PageLoadTime.json")


class Test_PageLoadTime:
    @staticmethod
    def auto_assign_allure_features(feature_string):
        import allure
        parts = feature_string.split('/')

        if len(parts) > 0:
            allure.dynamic.epic(f'{parts[0]}')
        if len(parts) > 1:
            allure.dynamic.feature(f'{parts[1]}')
        if len(parts) > 2:
            remaining_story = '/'.join(parts[2:])
            allure.dynamic.story(f'{remaining_story}')

    use_number_reload = getattr(Default, 'numberReload', 1)

    @pytest.mark.repeat(use_number_reload)
    @pytest.mark.LoadTime
    @pff.parametrize(path=pathDataTestLoadTime, key="test_page_load_time")
    def test_page_load_time(self, browser, feature, path_feature, expected_signals, steps):
        self.auto_assign_allure_features(feature)
        allure.dynamic.title(f"{feature}")
        allure.dynamic.description(f"Đo thời gian load trang: {feature}")
        driver = browser
        page_load_time = PageLoadTime(driver)
        default = Default()
        url = default.url

        with allure.step(f"Get URL: {feature}"):
            url_per = urljoin(url, path_feature)
            driver.get(url_per)
        with allure.step("Pre_Steps"):
            page_load_time.setup_steps_before_check(steps)
        with allure.step("Thời gian tải trang"):
            start_time = time.time()

            # Đảm bảo phần tử quan trọng hiển thị trên trang
            if not page_load_time.verify_signals_visibility(expected_signals, default.timeOut):
                raise AssertionError(f"Expected elements not visible within {default.timeOut} seconds.")

            # Đảm bảo không có loading trên web
            if not page_load_time.measure_page_load_time(default.timeOut):
                raise AssertionError(f"Page did not load within {default.timeOut} seconds.")

            load_time = time.time() - start_time

            # Đính kèm thời gian tải trang
            allure.attach(
                f"Page loaded in {load_time:.2f} seconds.",
                name="Page Load Time",
                attachment_type=allure.attachment_type.TEXT
            )
        capture_screenshot_and_attach_allure(driver, "Capture Image")
