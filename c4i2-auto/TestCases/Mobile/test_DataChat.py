import pytest
from faker import Faker
from datetime import datetime

fake = Faker()


@pytest.fixture(params=[fake.text().replace(" ", "")[:20]])
def RandomText(request):
    return request.param


def generate_channel_name(name):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d_%m_%H_%M")
    return f"{name}_{formatted_datetime}"


# Fixture để tạo dữ liệu test
@pytest.fixture
def test_chat_data():
    return generate_channel_name("Mobile")
