# 🏁 TEST DATA MANAGEMENT

Test data factories, seeders, and fixtures for consistent, maintainable test data.

## Features
- **Factory pattern** with trait system
- **API seeder** with auto-teardown context manager
- **Static fixtures** (JSON) for stable reference data
- **Security test data** -- SQL injection, XSS, empty fields
- Zero external deps (stdlib + requests only)

## Quick Start

```bash
pip install requests pytest
pytest tests/ -v
```

## Usage

```python
from factory.factories import UserFactory, ProductFactory, CredentialsFactory
from seeders.api_seeder import APISueder

# Build objects
user = UserFactory.build()
admin = UserFactory.admin()
users = UserFactory.build_batch(10)

# Seed via API with auto-cleanup
with APISeeder() as seeder:
    post = seeder.seed_post(userId=1)
    # ... tests ...
# teardown automatic
```

## Licence
MMIT
