from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from library import Library, Book as LibraryBook
from main import get_book_details_from_openlibrary
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# This dictionary will hold our single Library instance.
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs when the application starts up.
    print("Server starting up...")
    # Create the single, shared Library instance and store it in the app_state.
    app_state["library"] = Library()
    print(f"Library loaded with {len(app_state['library'].books)} books.")
    yield
    # This code runs when the application is shutting down.
    print("Server shutting down...")
    app_state["library"].save_books()
    print("Library data saved.")

app = FastAPI(
    title="Library API",
    description="A simple API to manage a library of books.",
    version="1.0.0",
    lifespan=lifespan # Use the lifespan manager
)

# Add CORS middleware to allow the HTML file to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Book(BaseModel):
    """Pydantic model for a book, used for API request and response validation."""
    title: str
    author: str
    isbn: str
    year: int
    available: bool = True
    # Add the new date field, make it optional for incoming requests
    date_added: Optional[str] = None

@app.get("/books", response_model=List[Book])
async def list_all_books():
    """Retrieve a list of all books in the library."""
    library = app_state["library"]
    return [book.to_dict() for book in library.books]

@app.get("/books/{isbn}", response_model=Book)
async def get_single_book(isbn: str):
    """Retrieve a single book by its ISBN."""
    library = app_state["library"]
    book = library.find_book(isbn)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict()

@app.get("/openlibrary/{isbn}")
async def fetch_openlibrary_info(isbn: str):
    """Fetch book details from OpenLibrary without adding to the library."""
    book_data = get_book_details_from_openlibrary(isbn)
    if not book_data:
        raise HTTPException(status_code=404, detail="Book not found on OpenLibrary.")
    return book_data

@app.post("/books", response_model=Book, status_code=201)
async def add_new_book(book: Book):
    """Add a new book to the library."""
    library = app_state["library"]
    if any(b.isbn == book.isbn for b in library.books):
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    new_book = LibraryBook(**book.model_dump(exclude_none=True))
    library.add_book(new_book)
    # Find the book again to get the version with the timestamp
    added_book = library.find_book(new_book.isbn)
    return added_book.to_dict()

@app.put("/books/{isbn}", response_model=Book)
async def update_existing_book(isbn: str, updated_book: Book):
    """Update an existing book's details."""
    library = app_state["library"]
    book_to_update = library.find_book(isbn)
    if book_to_update is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    update_data = updated_book.model_dump(exclude={'isbn'}, exclude_none=True)
    library.update_book(isbn, **update_data)
    
    updated_book_data = library.find_book(isbn)
    return updated_book_data.to_dict()

@app.delete("/books/{isbn}", status_code=204)
async def remove_existing_book(isbn: str):
    """Remove a book from the library."""
    library = app_state["library"]
    if not library.find_book(isbn):
        raise HTTPException(status_code=404, detail="Book not found")
    
    library.remove_book(isbn)
    return {}
