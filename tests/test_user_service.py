import pytest

from app.exceptions.user_error import DuplicateUsernameError, InvalidAmountError, InsufficientBalanceError


class TestUserServiceCreateUser:
    def test_create_user_success(self, temp_user_service):
        user = temp_user_service.create_user("legit_user", 150.0)
        assert user["user_id"] == 1
        assert user["username"] == "legit_user"
        assert user["balance"] == 150.0

    def test_cannot_create_duplicate_username(self, temp_user_service):
        temp_user_service.create_user("sigma_grind", 100.0)
        with pytest.raises(DuplicateUsernameError):
            temp_user_service.create_user("sigma_grind", 200.0)


class TestUserServiceBalanceOperations:
    def test_add_balance_success(self, temp_user_service):
        temp_user_service.create_user("rich_guy", 100.0)
        updated = temp_user_service.add_balance(50.0, user_id=1)
        assert updated["balance"] == 150.0

    def test_add_balance_negative_or_zero_raises_error(self, temp_user_service):
        temp_user_service.create_user("rich_guy", 100.0)
        with pytest.raises(InvalidAmountError):
            temp_user_service.add_balance(0, user_id=1)
        with pytest.raises(InvalidAmountError):
            temp_user_service.add_balance(-10.0, user_id=1)

    def test_remove_balance_success(self, temp_user_service):
        temp_user_service.create_user("broke_guy", 100.0)
        updated = temp_user_service.remove_balance(40.0, user_id=1)
        assert updated["balance"] == 60.0

    def test_remove_balance_negative_or_zero_raises_error(self, temp_user_service):
        temp_user_service.create_user("broke_guy", 100.0)
        with pytest.raises(InvalidAmountError):
            temp_user_service.remove_balance(0, user_id=1)
        with pytest.raises(InvalidAmountError):
            temp_user_service.remove_balance(-20.0, user_id=1)

    def test_remove_balance_prevent_negative_balance(self, temp_user_service):
        temp_user_service.create_user("broke_guy", 50.0)
        with pytest.raises(InsufficientBalanceError):
            temp_user_service.remove_balance(60.0, user_id=1)
