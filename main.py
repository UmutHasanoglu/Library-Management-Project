import httpx
import json
from library import Library, Book

def display_menu():
    """Displays the main menu of the library application."""
    print("\n--- Library Menu ---")
    print("1. Add a new book")
    print("2. Remove a book")
    print("3. List all books")
    print("4. Find a book by ISBN")
    print("5. Update a book")
    print("6. Add book from OpenLibrary")
    print("7. Exit")

def get_book_details_from_openlibrary(isbn: str):
    """
    Fetches book details from OpenLibrary using the most reliable search API.
    """
    search_api_url = f"https://openlibrary.org/search.json?isbn={isbn}"
    try:
        with httpx.Client() as client:
            response = client.get(search_api_url, follow_redirects=True)
            response.raise_for_status()
            data = response.json()

            # Check if any documents were found
            if data.get('numFound', 0) == 0 or not data.get('docs'):
                print(f"No book found with ISBN {isbn} on OpenLibrary.")
                return None

            # Use the first result
            book_data = data['docs'][0]
            
            title = book_data.get('title', 'N/A')
            author_names = ", ".join(book_data.get('author_name', ['N/A']))
            
            # The year is often the first published year
            year = book_data.get('first_publish_year', 0)

            return {
                'title': title,
                'author': author_names,
                'year': year,
                'isbn': isbn
            }
            
    except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Failed to fetch or parse data from OpenLibrary: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    """The main function to run the library application."""
    library = Library()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            try:
                year = int(input("Enter publication year: "))
                book = Book(title, author, isbn, year)
                library.add_book(book)
            except ValueError:
                print("Invalid year. Please enter a number.")

        elif choice == '2':
            isbn = input("Enter ISBN of the book to remove: ")
            library.remove_book(isbn)

        elif choice == '3':
            library.list_books()

        elif choice == '4':
            isbn = input("Enter ISBN of the book to find: ")
            book = library.find_book(isbn)
            if book:
                print(f"Found Book: {book.title} by {book.author}")
            else:
                print("Book not found.")

        elif choice == '5':
            isbn = input("Enter ISBN of the book to update: ")
            if library.find_book(isbn):
                print("Enter new details (leave blank to keep current value):")
                title = input(f"Title: ")
                author = input(f"Author: ")
                year_str = input(f"Year: ")
                
                update_data = {}
                if title:
                    update_data['title'] = title
                if author:
                    update_data['author'] = author
                if year_str:
                    try:
                        update_data['year'] = int(year_str)
                    except ValueError:
                        print("Invalid year format.")
                
                if update_data:
                    library.update_book(isbn, **update_data)
            else:
                print("Book not found.")

        elif choice == '6':
            isbn = input("Enter ISBN to fetch from OpenLibrary: ")
            book_data = get_book_details_from_openlibrary(isbn)
            if book_data:
                book = Book(**book_data)
                library.add_book(book)

        elif choice == '7':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
