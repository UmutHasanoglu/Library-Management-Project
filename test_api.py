import pytest
from fastapi.testclient import TestClient
import os
import json

# Import the app and the Library class
from api import app
from library import Library

@pytest.fixture
def client(monkeypatch, tmp_path):
    """
    This fixture creates a temporary, isolated environment for each test function.
    
    1.  `tmp_path`: A pytest fixture that creates a unique temporary directory.
    2.  `monkeypatch`: A pytest fixture to safely modify the behavior of our code for tests.
    """
    # Define the path for a temporary library file inside the temp directory
    test_library_path = tmp_path / "test_library.json"
    
    # Create an empty library file to start fresh
    test_library_path.write_text("[]", encoding="utf-8")

    # This is the magic: We tell our Library class to use the temporary file
    # instead of the real "library.json" whenever it's initialized during tests.
    # We define a proper function for __init__ that doesn't return a value.
    def mock_init(self, filename=str(test_library_path)):
        self.filename = filename
        self.books = self.load_books()

    monkeypatch.setattr(Library, '__init__', mock_init)

    # The 'with' statement ensures FastAPI's lifespan events run correctly
    # for a clean startup and shutdown within the test.
    with TestClient(app) as c:
        yield c

# All tests now take 'client' as an argument, which provides the isolated environment.

def test_list_all_books_empty(client):
    """Test listing books when the library is empty."""
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_add_new_book(client):
    """Test adding a new book via the API successfully."""
    book_data = {
        "title": "API Test Book",
        "author": "Tester",
        "isbn": "99999",
        "year": 2025
    }
    response = client.post("/books", json=book_data)
    assert response.status_code == 201
    assert response.json()["title"] == "API Test Book"

    list_response = client.get("/books")
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["isbn"] == "99999"

def test_add_duplicate_book_fails(client):
    """Test that adding a book with a duplicate ISBN results in a 400 error."""
    book_data = {"title": "Duplicate", "author": "Copy", "isbn": "11111", "year": 2025}
    
    response1 = client.post("/books", json=book_data)
    assert response1.status_code == 201

    response2 = client.post("/books", json=book_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]

def test_get_single_book(client):
    """Test retrieving a single book by its ISBN after adding it."""
    book_data = {"title": "Findable Book", "author": "Seeker", "isbn": "88888", "year": 2022}
    client.post("/books", json=book_data)
    
    response = client.get("/books/88888")
    assert response.status_code == 200
    assert response.json()["title"] == "Findable Book"

def test_get_nonexistent_book(client):
    """Test that trying to retrieve a book that doesn't exist returns a 404 error."""
    response = client.get("/books/00000")
    assert response.status_code == 404

def test_update_existing_book(client):
    """Test updating an existing book."""
    book_data = {"title": "Old Title", "author": "Old Author", "isbn": "77777", "year": 2021}
    client.post("/books", json=book_data)

    updated_data = {"title": "New Title", "author": "New Author", "isbn": "77777", "year": 2021, "available": False}
    response = client.put("/books/77777", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["available"] is False

def test_remove_existing_book(client):
    """Test removing a book."""
    book_data = {"title": "To Be Deleted", "author": "Deleter", "isbn": "66666", "year": 2020}
    client.post("/books", json=book_data)

    response = client.delete("/books/66666")
    assert response.status_code == 204

    get_response = client.get("/books/66666")
    assert get_response.status_code == 404
