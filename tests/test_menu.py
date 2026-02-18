"""Tests for the café menu."""

from menu import MAX_MENU_SIZE, MENU_ITEMS, get_categories, get_menu


def test_menu_items_have_required_fields():
    required = {"name", "category", "price", "description"}
    for item in MENU_ITEMS:
        assert required.issubset(item.keys()), f"{item.get('name', '?')} missing fields"


def test_prices_are_positive():
    for item in MENU_ITEMS:
        assert item["price"] > 0, f"{item['name']} has non-positive price"


def test_names_are_unique():
    names = [item["name"] for item in MENU_ITEMS]
    assert len(names) == len(set(names)), "Duplicate menu item names found"


def test_get_menu_returns_sorted():
    menu = get_menu()
    keys = [(item["category"], item["name"]) for item in menu]
    assert keys == sorted(keys)


def test_get_categories_returns_unique_sorted():
    cats = get_categories()
    assert cats == sorted(set(cats))


def test_no_empty_descriptions():
    for item in MENU_ITEMS:
        assert item["description"].strip(), f"{item['name']} has empty description"


def test_menu_size_within_limit():
    assert len(MENU_ITEMS) <= MAX_MENU_SIZE, (
        f"Menu has {len(MENU_ITEMS)} items but max is {MAX_MENU_SIZE}. "
        f"Increase MAX_MENU_SIZE or remove items before adding more."
    )


def test_average_price_reasonable():
    avg = sum(item["price"] for item in MENU_ITEMS) / len(MENU_ITEMS)
    assert avg <= 4.50, (
        f"Average menu price is ${avg:.2f}, which exceeds the $4.50 target. "
        f"Consider adding more affordable options."
    )
