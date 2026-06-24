# 🏭 Test Data Management

Factory pattern test data library for consistent, maintainable test data across all frameworks — zero Faker dependency, stdlib + requests only.

[![CI](https://github.com/sharika8/test-data-management/actions/workflows/tests.yml/badge.svg)](https://github.com/sharika8/test-data-management/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

| Feature | Detail |
|---|---|
| **Factory pattern** | Trait system — `UserFactory.admin()`, `ProductFactory.out_of_stock()` |
| **API seeder** | Context manager with auto-teardown — seed data, test, cleanup |
| **Static fixtures** | JSON fixtures for stable reference data |
| **Security payloads** | SQL injection, XSS, empty fields, long strings built-in |
| **Zero deps** | Stdlib + requests only — no Faker needed |
| **17 unit tests** | Full factory coverage — all passing in CI |

---

## 📁 Project Structure

```
test-data-management/
├── factory/
│   ├── base.py          # Factory base class + rand_str/email/uuid/date helpers
│   └── factories.py     # UserFactory, ProductFactory, OrderFactory, CredentialsFactory
├── seeders/
│   └── api_seeder.py    # HTTP API seeder with auto-teardown context manager
├── fixtures/
│   ├── loader.py        # Load JSON fixtures by name
│   └── users.json       # User data: valid, admin, invalid, injection payloads
└── tests/
    └── test_factories.py # 17 unit tests — all factories, all traits
```

---

## 🚀 Quick Start

```bash
pip install requests pytest

# Run tests
pytest tests/ -v
```

## 💡 Usage

```python
from factory.factories import UserFactory, ProductFactory, CredentialsFactory
from seeders.api_seeder import APISeeder
from fixtures.loader import load

# Build objects in memory (not persisted)
user    = UserFactory.build()
admin   = UserFactory.admin()
users   = UserFactory.build_batch(10)
oos     = ProductFactory.out_of_stock()

# All invalid credential combos (includes injection payloads)
invalid = CredentialsFactory.all_invalid()

# Seed via API with automatic teardown
with APISeeder() as seeder:
    post = seeder.seed_post(userId=1)
    # ... run tests ...
# teardown runs automatically

# Load static fixtures
fixture = load("users")
valid   = fixture["valid_login"]  # {"username": "tomsmith", "password": "..."}
```

---

## 🔗 Related Repos

| Repo | Description |
|---|---|
| [enterprise-qa-framework](https://github.com/sharika8/enterprise-qa-framework) | Python + Playwright |
| [snowflake-data-pipeline-tests](https://github.com/sharika8/snowflake-data-pipeline-tests) | Data pipeline DQ testing |
| [playwright-typescript-framework](https://github.com/sharika8/playwright-typescript-framework) | TypeScript UI + API |

---

## 📜 Licence
MIT