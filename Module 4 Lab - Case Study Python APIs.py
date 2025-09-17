from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        """Convert the Book object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'book_name': self.book_name,
            'author': self.author,
            'publisher': self.publisher
        }

# Create the database and tables
with app.app_context():
    db.create_all()

# ---- API ROUTES ----

# GET all books or POST a new book
@app.route('/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        data = request.json
        new_book = Book(
            book_name=data['book_name'],
            author=data['author'],
            publisher=data['publisher']
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201
    
    else:  # GET request
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books])

# GET, PUT, or DELETE a single book by ID
@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_book(id):
    book = Book.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(book.to_dict())

    elif request.method == 'PUT':
        data = request.json
        book.book_name = data.get('book_name', book.book_name)
        book.author = data.get('author', book.author)
        book.publisher = data.get('publisher', book.publisher)
        db.session.commit()
        return jsonify(book.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)