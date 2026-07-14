from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'maths'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'maths'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'maths'}
]

@app.get("/books")
def read_all_books():
    return BOOKS

# @app.get("/books/mybook")
# def read_all_books():
#     return {"title": "my fav book"}

@app.get("/books/{book_title}")
def read_all_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get("/books/")
def read_category_by_query(category: str):
    books = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books.append(book)
    return books

@app.get("/books/by_author/")
def fetch_books_by_author(author_name: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books.append(book)
    return books

@app.get("/books/{book_author}/")
def read_author_category_by_query(book_author: str, category: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books.append(book)
    return books

@app.post("/books/create_book")
def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if updated_book.get('title').casefold() == BOOKS[i]['title'].casefold():
            BOOKS[i] = updated_book

@app.delete("/books/delete_book/{book_title")
def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

@app.get("/books/by_author/{author_name}")
def fetch_books_by_author(author_name: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books.append(book)
    return books