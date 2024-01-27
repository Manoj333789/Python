from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data.db"
db=SQLAlchemy(app)




@app.route("/")
def index():
    return "Hello"

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display_info(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn}

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_all_books(self):
        l=[]
        for i in self.books:
            l.append(i)
        return l
    def delete_book(self,title):
        for i in self.books:
            if i.title == title:
                del i
                return "book deleted"

    def search_book_by_title(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return {"message": "Book Not Found"}

class EBook(Book):
    def __init__(self, title, author, isbn, file_format):
        super().__init__(title, author, isbn)
        self.file_format = file_format

    def display_info(self):
        info = super().display_info()
        info["file_format"] = self.file_format
        return info

library = Library()

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    try:
        if data.get("file_format"):
            book = EBook(data["title"], data["author"], data["isbn"], data["file_format"])
        else:
            book = Book(data["title"], data["author"], data["isbn"])

        library.add_book(book)
        return jsonify({"message": "Book added successfully!"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

@app.route('/books', methods=['GET'])
def get_all_books():
    return jsonify(library.display_all_books())

@app.route('/books/<title>', methods=['GET'])
def search_book(title):
    result = library.search_book_by_title(title)
    return jsonify(result)

@app.route('/books/<title>', methods=['DElETE'])
def delete_book(title):
    result = library.delete_book(title)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

