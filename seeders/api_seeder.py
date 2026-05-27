"""seeders/api_seeder.py - Seed test data via HTTP API"""
import requests
from factory.factories import APIPostFactory


class APISeeder:
    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"
        self._created = {"posts": []}

    def seed_post(self, **overrides):
        payload = {**APIPostFactory.build(), **overrides}
        r = self.session.post(f"{self.base_url}/posts", json=payload)
        r.raise_for_status()
        created = r.json()
        self._created["posts"].append(created.get("id"))
        return created

    def seed_posts(self, n=5, **overrides):
        return [self.seed_post(**overrides) for _ in range(n)]

    def teardown(self):
        for post_id in self._created["posts"]:
            try: self.session.delete(f"{self.base_url}/posts/{post_id}")
            except Exception: pass
        self._created = {"posts": []}

    def __enter__(self): return self
    def __exit__(self, *_): self.teardown()
