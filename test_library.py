import pytest
import os
from library import Book, Library

@pytest.fixture
def library_fixture():
    """Fixture to create a temporary library for testing."""
    test_library = Library(filename="test_library.json")
    yield test_library
    # Teardown: remove the test file after tests are done
    if os.path.exists("test_library.json"):
        os.remove("test_library.json")

def test_add_book(library_fixture):
    """Test adding a new book."""
    book = Book("Test Title", "Test Author", "12345", 2023)
    library_fixture.add_book(book)
    assert len(library_fixture.books) == 1
    assert library_fixture.books[0].title == "Test Title"

def test_remove_book(library_fixture):
    """Test removing an existing book."""
    book = Book("Another Title", "Another Author", "67890", 2024)
    library_fixture.add_book(book)
    library_fixture.remove_book("67890")
    assert len(library_fixture.books) == 0

def test_find_book(library_fixture):
    """Test finding a book by ISBN."""
    book = Book("Find Me", "Finder", "11223", 2021)
    library_fixture.add_book(book)
    found_book = library_fixture.find_book("11223")
    assert found_book is not None
    assert found_book.title == "Find Me"

def test_update_book(library_fixture):
    """Test updating a book's details."""
    book = Book("Original Title", "Original Author", "44556", 2020)
    library_fixture.add_book(book)
    library_fixture.update_book("44556", title="Updated Title")
    updated_book = library_fixture.find_book("44556")
    assert updated_book.title == "Updated Title"

