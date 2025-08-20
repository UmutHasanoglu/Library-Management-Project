import json
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Book:
    """Represents a single book in the library."""
    title: str
    author: str
    isbn: str
    year: int
    available: bool = True
    # New field to track when the book was added
    date_added: str = None

    def to_dict(self):
        """Converts the Book object to a dictionary."""
        return asdict(self)

class Library:
    """Manages the collection of books in the library."""

    def __init__(self, filename="library.json"):
        """Initializes the Library, loading books from the specified file."""
        self.filename = filename
        self.books = self.load_books()

    def add_book(self, book: Book):
        """Adds a new book to the library if the ISBN doesn't already exist."""
        if any(b.isbn == book.isbn for b in self.books):
            print(f"Error: Book with ISBN {book.isbn} already exists.")
            return False
        
        # Set the date_added timestamp for the new book
        book.date_added = datetime.now().isoformat()
        
        self.books.append(book)
        self.save_books()
        print(f"Book '{book.title}' added successfully.")
        return True

    def remove_book(self, isbn: str):
        """Removes a book from the library by its ISBN."""
        initial_count = len(self.books)
        self.books = [book for book in self.books if book.isbn != isbn]
        if len(self.books) < initial_count:
            self.save_books()
            print(f"Book with ISBN {isbn} removed successfully.")
        else:
            print(f"Error: Book with ISBN {isbn} not found.")

    def list_books(self):
        """Lists all the books in the library."""
        if not self.books:
            print("The library is empty.")
            return
        for book in self.books:
            status = "Available" if book.available else "Checked Out"
            print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Year: {book.year}, Status: {status}")

    def find_book(self, isbn: str):
        """Finds and returns a book by its ISBN."""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def update_book(self, isbn: str, **kwargs):
        """Updates the details of a book identified by its ISBN."""
        book_to_update = self.find_book(isbn)
        if book_to_update:
            for key, value in kwargs.items():
                if hasattr(book_to_update, key):
                    setattr(book_to_update, key, value)
            self.save_books()
            print(f"Book with ISBN {isbn} updated successfully.")
        else:
            print(f"Error: Book with ISBN {isbn} not found.")

    def load_books(self):
        """Loads books from the JSON file, ensuring UTF-8 encoding is used."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                books_data = json.load(f)
                loaded_books = []
                for data in books_data:
                    # For backward compatibility, add a default date if it's missing
                    if 'date_added' not in data:
                        data['date_added'] = datetime(1970, 1, 1).isoformat()
                    loaded_books.append(Book(**data))
                return loaded_books
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self):
        """Saves the current list of books to the JSON file using UTF-8."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4, ensure_ascii=False)
