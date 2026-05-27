"""
factory/base.py - Core data factory with trait system
"""
from __future__ import annotations
import random
import string
import uuid
from datetime import datetime, timedelta
from typing import Any, Callable


class Factory:
    """Base factory class. Subclass and define _defaults() to create typed factories."""

    _overrides: dict = {}
    _traits: dict[str, dict] = {}
    _sequence_counters: dict[str, int] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._overrides = {}
        cls._traits = {}
        cls._sequence_counters = {}

    @classmethod
    def _defaults(cls) -> dict:
        raise NotImplementedError("Subclass must implement _defaults()")

    @classmethod
    def _next_seq(cls, key: str) -> int:
        cls._sequence_counters[key] = cls._sequence_counters.get(key, 0) + 1
        return cls._sequence_counters[key]

    @classmethod
    def build(cls, **kwargs) -> dict:
        data = cls._defaults()
        data.update(kwargs)
        return {k: v() if callable(v) else v for k, v in data.items()}

    @classmethod
    def build_batch(cls, size: int, **kwargs) -> list:
        return [cls.build(**kwargs) for _ in range(size)]

    @classmethod
    def reset_sequences(cls) -> None:
        cls._sequence_counters.clear()


def rand_str(length=8, prefix=""):
    return prefix + "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

def rand_email(domain="test.example.com"):
    return f"{rand_str(8)}@{domain}"

def rand_name():
    first = random.choice(["Alice","Bob","Carol","Dave","Eve","Frank","Grace","Henry"])
    last  = random.choice(["Smith","Jones","Williams","Brown","Wilson","Taylor","Davies"])
    return f"{first} {last}"

def rand_uuid(): return __import__("uuid").uuid4().__str__()
def rand_int(lo=1, hi=1000): return random.randint(lo, hi)
def rand_float(lo=0.0, hi=100.0, d=2): return round(random.uniform(lo, hi), d)
def rand_bool(): return random.choice([True, False])
def rand_phone(): return f"+44 {random.randint(7000,7999)} {random.randint(100000,999999)}"
def rand_date(days_back=365):
    from datetime import datetime, timedelta
    return (datetime.now() - timedelta(days=random.randint(0, days_back))).strftime("%Y-%m-%d")
def rand_datetime(days_back=365):
    from datetime import datetime, timedelta
    d = timedelta(days=random.randint(0, days_back), seconds=random.randint(0,86400))
    return (datetime.now() - d).isoformat()
def rand_address():
    return {"street":f"{random.randint(1,200)} {random.choice(['Main','High'])} St","city":random.choice(["London","Manchester","Leeds"]),"country":"GB"}
