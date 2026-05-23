import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from repositories.item_repo import ItemRepo
from repositories.listing_repo import ListingRepo
from repositories.user_repo import UserRepo
from services.item_service import ItemService
from services.listing_service import ListingService
from services.user_service import UserService
from services.market_service import MarketService


@pytest.fixture
def temp_item_repo(tmp_path):
    repo = ItemRepo()
    repo.filepath = str(tmp_path / "items.json")
    with open(repo.filepath, "w") as json_file:
        json.dump([], json_file)
    return repo


@pytest.fixture
def temp_listing_repo(tmp_path):
    repo = ListingRepo()
    repo.filepath = str(tmp_path / "listings.json")
    with open(repo.filepath, "w") as json_file:
        json.dump([], json_file)
    return repo


@pytest.fixture
def temp_user_repo(tmp_path):
    repo = UserRepo()
    repo.filepath = str(tmp_path / "users.json")
    with open(repo.filepath, "w") as json_file:
        json.dump([], json_file)
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


@pytest.fixture
def temp_user_service(temp_user_repo):
    service = UserService()
    service.user_repo = temp_user_repo
    return service


@pytest.fixture
def temp_market_service(
    temp_item_repo, temp_listing_repo, temp_user_service, temp_item_service, temp_listing_service
):
    service = MarketService()
    service.user_service = temp_user_service
    service.item_service = temp_item_service
    service.listing_service = temp_listing_service
    return service
