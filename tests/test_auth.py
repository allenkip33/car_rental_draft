import os

import pytest

from services.auth import AuthService
from services.data_manager import DataManager

TEST_USERS_FILE = "data/test_users.json"


@pytest.fixture(autouse=True)
def cleanup_test_users_file():
    yield
    if os.path.exists(TEST_USERS_FILE):
        os.remove(TEST_USERS_FILE)


def test_register_user():
    manager = DataManager()
    auth = AuthService(manager, TEST_USERS_FILE)

    result = auth.register("testuser", "password123")

    assert result is True


def test_login_user():
    manager = DataManager()
    auth = AuthService(manager, TEST_USERS_FILE)

    auth.register("testuser2", "password123")
    user = auth.login("testuser2", "password123")

    assert user.username == "testuser2"


def test_wrong_password():
    manager = DataManager()
    auth = AuthService(manager, TEST_USERS_FILE)

    auth.register("testuser3", "password123")
    user = auth.login("testuser3", "wrongpassword")

    assert user is None
