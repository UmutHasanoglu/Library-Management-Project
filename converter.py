import json
from datetime import datetime

def convert_library_format(input_filename, output_filename):
    """
    Converts a LibraryThing JSON export to the format used by our app,
    ensuring correct handling of UTF-8 characters and adding the date_added field.
    """
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file '{input_filename}' is not a valid JSON file.")
        return

    converted_books = []
    for book_id, book_data in data.items():
        title = book_data.get('title', 'N/A')
        author = book_data.get('primaryauthor', 'N/A')
        
        isbn_info = book_data.get('isbn')
        isbn = "N/A"
        if isinstance(isbn_info, dict):
            isbn = isbn_info.get('0', 'N/A')
        elif isinstance(isbn_info, list) and isbn_info:
            isbn = isbn_info[0]
        elif isinstance(isbn_info, str):
            isbn = isbn_info
        
        if isbn == "N/A" and 'originalisbn' in book_data:
            isbn = book_data['originalisbn']

        try:
            year = int(book_data.get('date', '0'))
        except (ValueError, TypeError):
            year = 0
            
        # Use the 'entrydate' from the original file for the 'date_added' field
        # This provides a more meaningful timestamp for your existing books.
        date_added_str = book_data.get('entrydate', datetime.now().strftime('%Y-%m-%d'))
        try:
            # Convert to ISO format for consistent sorting
            date_added_iso = datetime.strptime(date_added_str, '%Y-%m-%d').isoformat()
        except ValueError:
            date_added_iso = datetime.now().isoformat()


        new_book = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "year": year,
            "available": True,
            "date_added": date_added_iso
        }
        converted_books.append(new_book)

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(converted_books, f, indent=4, ensure_ascii=False)
        print(f"Successfully converted {len(converted_books)} books.")
        print(f"New file saved as '{output_filename}'")
    except IOError as e:
        print(f"Error writing to file '{output_filename}': {e}")


if __name__ == "__main__":
    convert_library_format('librarything_umuthasanoglu.json', 'library.json')
