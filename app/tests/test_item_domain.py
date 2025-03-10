import pytest

from app.core.domain.item import Item


def test_item_creation():
    """Test that an item can be created with the correct attributes."""
    item = Item(name="Test Item", description="A test item", price=10.0)

    assert item.name == "Test Item"
    assert item.description == "A test item"
    assert item.price == 10.0
    assert item.is_active is True


def test_item_apply_discount():
    """Test that the apply_discount method works correctly."""
    item = Item(name="Test Item", price=100.0)

    # Apply 20% discount
    discounted_price = item.apply_discount(20)

    assert discounted_price == 80.0
    # Original price should not be modified
    assert item.price == 100.0


def test_item_apply_discount_invalid():
    """Test that apply_discount raises an error for invalid discount values."""
    item = Item(name="Test Item", price=100.0)

    # Test with negative discount
    with pytest.raises(ValueError):
        item.apply_discount(-10)

    # Test with discount > 100
    with pytest.raises(ValueError):
        item.apply_discount(110)
