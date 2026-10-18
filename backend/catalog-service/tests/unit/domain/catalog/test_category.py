import pytest

from catalog_api.domain.catalog.entities import Category
from catalog_api.domain.catalog.errors import (
    CategoryAlreadyExistsError,
    CategoryNameEmptyError,
    CategoryNameTooLongError,
    CategoryNameTooShortError,
    CategoryOldNameEquivalentNewNameError,
)
from catalog_api.domain.catalog.value_objects import CategoryID


@pytest.mark.parametrize("name", ["", " ", "\t", "\n", "\r\n", " \t\n "])
def test_category_rejects_empty_or_whitespace_name(name: str) -> None:
    with pytest.raises(CategoryNameEmptyError):
        Category(id=CategoryID.new(), name=name)


@pytest.mark.parametrize(
    ("name", "expected_name"),
    [
        ("ab", "ab"),
        ("a" * 32, "a" * 32),
        ("\t ab \n", "ab"),
    ],
)
def test_category_accepts_name_boundaries_and_strips_whitespace(
    name: str,
    expected_name: str,
) -> None:
    category = Category(id=CategoryID.new(), name=name)

    assert category.name == expected_name


@pytest.mark.parametrize("name", ["a", " \ta\n "])
def test_category_rejects_name_shorter_than_two_characters(name: str) -> None:
    with pytest.raises(CategoryNameTooShortError):
        Category(id=CategoryID.new(), name=name)


@pytest.mark.parametrize("name", ["a" * 33, "a" * 33 + " "])
def test_category_rejects_name_longer_than_32_characters(name: str) -> None:
    with pytest.raises(CategoryNameTooLongError):
        Category(id=CategoryID.new(), name=name)


@pytest.mark.parametrize(
    ("already_exists", "expected_error"),
    [
        (False, None),
        (True, CategoryAlreadyExistsError),
    ],
)
def test_category_checks_uniqueness(
    already_exists: bool,
    expected_error: type[Exception] | None,
) -> None:
    category = Category(id=CategoryID.new(), name="Category")

    if expected_error is None:
        category.is_unique(already_exists)
    else:
        with pytest.raises(expected_error, match="Category 'Category' already exists."):
            category.is_unique(already_exists)


@pytest.mark.parametrize(
    ("current_name", "updated_name", "expected_error"),
    [
        ("Category", "Category", CategoryOldNameEquivalentNewNameError),
        ("Category", "New category", None),
    ],
)
def test_category_rename_validates_name_change(
    current_name: str,
    updated_name: str,
    expected_error: type[Exception] | None,
) -> None:
    category = Category(id=CategoryID.new(), name=current_name)

    if expected_error is None:
        category.rename(current_name, updated_name)
    else:
        with pytest.raises(expected_error):
            category.rename(current_name, updated_name)
