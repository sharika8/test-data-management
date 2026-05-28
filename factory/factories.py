from __future__ import annotations
import random
from factory.base import Factory, rand_str, rand_email, rand_name, rand_uuid, rand_int, rand_float, rand_datetime, rand_address


class UserFactory(Factory):
    @classmethod
    def _defaults(cls):
        return {
            "id": lambda: rand_uuid(),
            "username": lambda: rand_str(8, "user_"),
            "email": lambda: rand_email(),
            "name": lambda: rand_name(),
            "role": "user",
            "active": True,
            "created_at": lambda: rand_datetime(),
        }

    @classmethod
    def admin(cls, **kwargs):
        return cls.build(role="admin", **kwargs)

    @classmethod
    def inactive(cls, **kwargs):
        return cls.build(active=False, **kwargs)

    @classmethod
    def locked(cls, **kwargs):
        return cls.build(active=False, locked=True, locked_reason="too_many_attempts", **kwargs)


class ProductFactory(Factory):
    CATEGORIES = ["electronics", "clothing", "books", "home", "sports"]

    @classmethod
    def _defaults(cls):
        return {
            "id": lambda: rand_uuid(),
            "sku": lambda: "SKU-" + rand_str(6).upper(),
            "name": lambda: "Product " + rand_str(4),
            "price": lambda: rand_float(1.0, 999.99),
            "stock": lambda: rand_int(0, 500),
            "active": True,
            "category": lambda: random.choice(ProductFactory.CATEGORIES),
        }

    @classmethod
    def out_of_stock(cls, **kwargs):
        return cls.build(stock=0, **kwargs)

    @classmethod
    def expensive(cls, **kwargs):
        return cls.build(price=rand_float(500, 9999.99), **kwargs)

    @classmethod
    def in_category(cls, cat, **kwargs):
        return cls.build(category=cat, **kwargs)


class OrderFactory(Factory):
    @classmethod
    def _defaults(cls):
        items = [ProductFactory.build() for _ in range(rand_int(1, 5))]
        return {
            "id": lambda: rand_uuid(),
            "items": items,
            "total": round(sum(i["price"] for i in items), 2),
            "status": "pending",
        }

    @classmethod
    def completed(cls, **kwargs):
        return cls.build(status="delivered", **kwargs)

    @classmethod
    def with_n_items(cls, n, **kwargs):
        items = [ProductFactory.build() for _ in range(n)]
        return cls.build(items=items, total=round(sum(i["price"] for i in items), 2), **kwargs)


class APIPostFactory(Factory):
    @classmethod
    def _defaults(cls):
        return {
            "userId": lambda: rand_int(1, 10),
            "title": lambda: rand_str(5),
            "body": lambda: rand_str(30),
        }


class APICommentFactory(Factory):
    @classmethod
    def _defaults(cls):
        return {
            "postId": lambda: rand_int(1, 100),
            "name": lambda: rand_str(10),
            "email": lambda: rand_email(),
            "body": lambda: rand_str(20),
        }


class CredentialsFactory(Factory):
    VALID = [{"username": "tomsmith", "password": "SuperSecretPassword!"}]
    INVALID = [
        {"username": "nobody", "password": "wrong"},
        {"username": "", "password": "SuperSecretPassword!"},
        {"username": "tomsmith", "password": ""},
        {"username": "", "password": ""},
        {"username": "sql OR 1=1", "password": "injection"},
        {"username": "xss_test", "password": "xss"},
    ]

    @classmethod
    def _defaults(cls): return cls.VALID[0]

    @classmethod
    def valid(cls, i=0): return cls.VALID[i % len(cls.VALID)]

    @classmethod
    def invalid(cls, i=0): return cls.INVALID[i % len(cls.INVALID)]

    @classmethod
    def all_invalid(cls): return list(cls.INVALID)