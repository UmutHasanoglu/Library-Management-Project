import pytest
from unittest.mock import patch, MagicMock
import httpx
from main import get_book_details_from_openlibrary

@patch('main.httpx.Client')
def test_get_book_details_from_openlibrary_success(mock_client):
    """Test fetching book details successfully using the search API."""
    isbn = '1234567890'
    # Mock the response from the /search.json endpoint
    mock_api_response = {
        "numFound": 1,
        "docs": [
            {
                "title": "Test Book",
                "author_name": ["Test Author"],
                "first_publish_year": 2023
            }
        ]
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_api_response
    
    mock_client.return_value.__enter__.return_value.get.return_value = mock_response

    book_details = get_book_details_from_openlibrary(isbn)
    
    assert book_details is not None
    assert book_details['title'] == 'Test Book'
    assert book_details['author'] == 'Test Author'
    assert book_details['year'] == 2023

@patch('main.httpx.Client')
def test_get_book_details_not_found(mock_client):
    """Test the case where the book is not found on OpenLibrary."""
    isbn = '0000000000'
    mock_api_response = {"numFound": 0, "docs": []}

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_api_response

    mock_client.return_value.__enter__.return_value.get.return_value = mock_response

    book_details = get_book_details_from_openlibrary(isbn)
    assert book_details is None

@patch('main.httpx.Client')
def test_get_book_details_api_failure(mock_client):
    """Test handling of failures when the API call fails."""
    # Raise an httpx error that the function is designed to catch.
    mock_client.return_value.__enter__.return_value.get.side_effect = httpx.RequestError("Mocked network error")

    book_details = get_book_details_from_openlibrary('0987654321')
    assert book_details is None
