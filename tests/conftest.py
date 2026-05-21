import json
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.repositories.item_repo import ItemRepo
from app.repositories.listing_repo import ListingRepo
from app.services.item_service import ItemService
from app.services.listing_service import ListingService


@pytest.fixture
def temp_item_repo(tmp_path):
    repo = ItemRepo()
    repo.filepath = str(tmp_path / "items.json")
    with open(repo.filepath, "w") as f:
        json.dump([], f)
    return repo


@pytest.fixture
def temp_listing_repo(tmp_path):
    repo = ListingRepo()
    repo.filepath = str(tmp_path / "listings.json")
    with open(repo.filepath, "w") as f:
        json.dump([], f)
    return repo


@pytest.fixture
def temp_item_service(temp_item_repo):
    service = ItemService()
    service.item_repo = temp_item_repo
    return service


@pytest.fixture
def temp_listing_service(temp_item_repo, temp_listing_repo):
    service = ListingService()
    service.item_repo = temp_item_repo
    service.listing_repo = temp_listing_repo
    return service
