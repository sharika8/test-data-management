"""Unit tests for data factories"""
import pytest
from factory.factories import UserFactory, ProductFactory, OrderFactory, APIPostFactory, CredentialsFactory


class TestUserFactory:
    def test_build(self): assert isinstance(UserFactory.build(), dict)
    def test_required_fields(self):
        u = UserFactory.build()
        for f in ("id", "username", "email", "name", "role", "active"):
            assert f in u, f"Missing: {f}"
    def test_email(self): assert "@" in UserFactory.build()["email"]
    def test_batch_unique(self):
        users = UserFactory.build_batch(5)
        assert len({u["id"] for u in users}) == 5
    def test_override(self): assert UserFactory.build(role="admin")["role"] == "admin"
    def test_admin_trait(self): assert UserFactory.admin()["role"] == "admin"
    def test_inactive_trait(self): assert UserFactory.inactive()["active"] is False
    def test_locked_trait(self): assert UserFactory.locked()["locked"] is True


class TestProductFactory:
    def test_price_positive(self): assert ProductFactory.build()["price"] > 0
    def test_out_of_stock(self): assert ProductFactory.out_of_stock()["stock"] == 0
    def test_expensive(self): assert ProductFactory.expensive()["price"] >= 500
    def test_category(self): assert ProductFactory.in_category("electronics")["category"] == "electronics"


class TestOrderFactory:
    def test_has_items(self):
        order = OrderFactory.build()
        assert isinstance(order["items"], list)
        assert len(order["items"]) >= 1
    def test_completed(self): assert OrderFactory.completed()["status"] == "delivered"
    def test_n_items(self): assert len(OrderFactory.with_n_items(3)["items"]) == 3


class TestAPIPostFactory:
    def test_has_fields(self):
        p = APIPostFactory.build()
        for f in ("userId", "title", "body"):
            assert f in p
    def test_user_id_range(self): assert 1 <= APIPostFactory.build()["userId"] <= 10


class TestCredentials:
    def test_valid(self):
        c = CredentialsFactory.valid()
        assert c["username"] and c["password"]
    def test_all_invalid_has_empty(self):
        assert any(c["username"] == "" for c in CredentialsFactory.all_invalid())
    def test_invalid_count(self):
        assert len(CredentialsFactory.all_invalid()) >= 4
