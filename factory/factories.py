"""factory/factories.py - Domain factories"""
from __future__ import annotations
import random
from factory.base import Factory, rand_str, rand_email, rand_name, rand_uuid, rand_int, rand_float, rand_datetime, rand_address


class UserFactory(Factory):
    @classmethod
    def _defaults(cls):
        return {
            "id": lambda: rand_uuid(), "username": lambda: rand_str(8, "user_"),
            "email": lambda: rand_email(), "name": lambda: rand_name(),
            "role": "user", "active": True, "created_at": lambda: rand_datetime(),
        }
    @classmethod
    def admin(cls, **kw): return cls.build(role="admin", **�w)
    @classmethod
    def inactive(cls, **�w): return cls.build(active=False, **kw)
    @classmethod
    def locked(cls, **�w): return cls.build(active=False, locked=True, locked_reason="too_many_attempts", **kw)


class ProductFactory(Factory):
    CATEGORIES = ["electronics", "clothing", "books", "home", "sports"]
    @classmethod
    def _defaults(cls):
        return {
            "id": lambda: rand_uuid(), "sku": lambda: f"SKU-{rand_str(6).upper()}",
            "name": lambda: f"Product {rand_str(4)}", "price": lambda: rand_float(1, 999.99),
            "stock": lambda: rand_int(0, 500), "active": True,
            "category": lambda: random.choice(ProductFactory.CATEGORIES),
        }
    @classmethod
    def out_of_stock(cls, **kw): return cls.build(stock=0, **kw)
    @classmethod
    def expensive(cls, **�w): return cls.build(price=rand_float(500, 9999.99), **kw)
    @classmethod
    def in_category(cls, cat, **kw): return cls.build(category=cat, **kw)


class OrderFactory(Factory):
    @classmethod
    def _defaults(cls):
        items = [ProductFactory.build() for _ in range(rand_int(1, 5))]
        return {"id": lambda: rand_uuid(), "items": items, "total": round(sum(i["price"] for i in items), 2), "status": "pending"}
    @classmethod
    def completed(cls, **kw): return cls.build(status="delivered", **kw)
    @classmethod
    def with_n_items(cls, n, **kw):
        items = [ProductFactory.build() for _ in range(n)}
        return cls.build(items=items, total=round(sum(i["price"] for i in items), 2), **kw)


class APIPostFactory(Factory):
    @classmethod
    def _defaults(cls):
        return {"userId": lambda: rand_int(1, 10), "title": lambda: rand_str(5),"body": lambda: rand_str(30)}


class APICommentFactory(Factory):
    @classmethod
    def _defaults(cls):
        return {"postId": lambda: rand_int(1,100), "name": lambda: rand_str(10), "email": lambda: rand_email(), "body": lambda: rand_str(20)}


class CredentialsFactory(Factory):
    VALID = [{"username": "tomsmith", "password": "SuperSecretPassword!"}]
    INVALID = [
        {"username": "nobody", "password": "wrong"},
        {"username": "", "password": "SuperSecretPassword!"},
        {"username": "tomsmith", "password": ""},
        {"username": "", "password": ""},
        {"username": "sql' OR '1'='1", "password": "injection"},
        {"username": "<script>alert(1)</script>", "password": "xss"},
    ]
    @classmethod
    def _defaults(cls): return cls.VALID[0]
    @classmethod
    def valid(cls, i=0): return cls.VALID[i % len(cls.VALID)]
    @classmethod
    def invalid(cls, i=0): return cls.INVALID[i % len(cls.INVALID)]
    @classmethod
    def all_invalid(cls): return cls.INVALID.copy()
