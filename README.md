# **Library Management System 📚**

Welcome to the Library Management System, a comprehensive Python project that evolves from a simple command-line tool into a full-fledged web application with a RESTful API backend. This project is designed to showcase key concepts in Object-Oriented Programming (OOP), API integration, web development, and testing.

## **✨ Features**

This application is built in three main parts, each adding a new layer of functionality:

### **Part 1: The Core Library (CLI)**

* **Add, Remove, List, and Find Books**: Core library management from the command line.  
* **Persistent Storage**: Book data is saved to and loaded from a library.json file.  
* **Object-Oriented**: Built with Book and Library classes to model the system.

### **Part 2: External API Integration**

* **OpenLibrary Integration**: Fetch book details automatically using an ISBN, enriching the library's data from an external source.  
* **Robust Fallbacks**: Implements a reliable, multi-step process to find book data even when primary API endpoints fail.

### **Part 3: Web Application & REST API**

* **FastAPI Backend**: A powerful and fast RESTful API for all library operations.  
* **Interactive Web UI**: A clean, responsive user interface built with HTML and Tailwind CSS.  
* **Dynamic Search & Sort**: Instantly search the entire collection and sort by title, author, year, or date added.  
* **Two-Step Book Fetching**: Fetch and review book info from OpenLibrary before adding it to your collection.  
* **Edit Functionality**: Update book details directly from the web interface through a pop-up modal.  
* **CSV Export**: Download your entire library collection as a .csv file with a single click.

## **🛠️ Tech Stack**

* **Backend**: Python, FastAPI  
* **Frontend**: HTML, JavaScript, Tailwind CSS  
* **Data Storage**: JSON  
* **API Interaction**: httpx  
* **Data Validation**: Pydantic  
* **Testing**: pytest  
* **Virtual Environment**: venv (or uv as per project spec)

## **🚀 Getting Started**

Follow these steps to get the project up and running on your local machine.

### **1\. Prerequisites**

* Python 3.8+  
* A virtual environment tool like venv or uv.

### **2\. Installation & Setup**

**Clone the repository:**

```bash
git clone https://github.com/UmutHasanoglu/Library-Management-Project.git

cd Library-Management-Project
```

**Create and activate a virtual environment:**

\# Using venv (standard library)  
```
python \-m venv .venv  
source .venv/bin/activate 
```
\# On Windows: 
```
.venv\\Scripts\\activate
```

\# Using uv (faster and modern)  
```
uv venv
```
Activate with: 
```
.venv\Scripts\activate
```

**Install the required dependencies:**
```
pip install \-r requirements.txt
```
or
```
uv pip install \-r requirements.txt
```

### **3\. Populating Your Library (Optional)**

The application uses library.json for storage. You can start with an empty library or use the included converter.py script to convert a LibraryThing JSON export into the correct format.

\# This will convert your export and create a pre-populated library.json  
```
python converter.py
```

## **⚙️ Usage Guide**

You can run the application in three different ways:

### **1\. Command-Line Interface (CLI)**

For basic, terminal-based library management:

```
python main.py
```

You will be presented with a menu of options to manage your library.

### **2\. FastAPI Web Service**

To run the backend API server:

```
uvicorn api:app \--reload
```

The API will be running at http://127.0.0.1:8000. 
You can access the interactive API documentation (powered by Swagger UI) at http://127.0.0.1:8000/docs.

### **3\. Web User Interface (UI)**

To use the full-featured web application:

1. Ensure the FastAPI Web Service is running (see step above).  
2. Open the index.html file directly in your web browser.

### **Windows Automation Scripts**

To make the project easier to use on Windows, three batch (.bat) scripts are included:

*install.bat*: This script will automatically create a virtual environment using uv, activate it, and install all the necessary dependencies from requirements.txt. Simply double-click this file to set up the project.

*start\_cli.bat*: This script runs the command-line interface (CLI) version. It automatically activates the virtual environment and runs python main.py.

*start\_webui.bat*: This script launches the FastAPI backend server and simultaneously opens the index.html web interface in your default web browser.

---

## **📖 API Documentation**

The API provides the following endpoints to interact with the library:

| Method | Path | Description |
| :---- | :---- | :---- |
| GET | /books | Retrieves a list of all books in the library. |
| GET | /books/{isbn} | Retrieves a single book by its ISBN. |
| GET | /openlibrary/{isbn} | Fetches book data from OpenLibrary without saving. |
| POST | /books | Adds a new book to the library. |
| PUT | /books/{isbn} | Updates the details of an existing book. |
| DELETE | /books/{isbn} | Removes a book from the library by its ISBN. |

## **✅ Testing**

The project includes a comprehensive test suite using `pytest` to ensure all components work as expected. The tests cover the core `Library` class logic, the `main` application functions, and all API endpoints.

**To run the tests:**
```bash
pytest
```
The tests are designed to be fully isolated and will not interfere with your `library.json` data file. They use temporary files and directories to ensure a clean state for every test run.