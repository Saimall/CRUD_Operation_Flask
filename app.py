import string
from flask import Flask, jsonify, request;
import csv;

#creating app object
app = Flask(__name__)

# Assigning the the csv file to csv_file name varibale
csv_filepath = 'books.csv'

#function which handles the write functionality
def write_file_csv(books_data):
    columnnames = ['id', 'title','author', 'gener', 'publication_year']
    with open(csv_filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columnnames)
        writer.writeheader()
        writer.writerows(books_data)

#function to read data from CSV file
def read_file_csv():
    with open(csv_filepath, 'r') as file:
        reader = csv.DictReader(file)
        books_list = list(reader)
    return books_list

# retriving all the data present in the books excel and returing in json 
@app.route('/books', methods=['GET'])
def getbooksdata():
    books_list = read_file_csv()
    return jsonify(books_list), 200


# retrive the book with the given ID  
@app.route('/books/<string:book_id>', methods=['GET'])
def getbookdata(book_id):
    books = read_file_csv()
    print(books)
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200

    return jsonify({'message': 'Seesms like book not found'}), 404

#storing or inserting the book deatiles using post request
@app.route('/books', methods=['POST'])
def create_book():
    bookslist = read_file_csv()
    new_book_data = {
        'id': request.json['id'],
        'title': request.json['title'],
        'author': request.json['author'],
        'gener': request.json['gener'],
        'publication_year':request.json['publication_year']
    }
    for book in bookslist:
        if int(book['id']) == int(new_book_data['id']):
            return jsonify("error book already existed with the given id")

    bookslist.append(new_book_data)
    write_file_csv(bookslist)
    return jsonify({'message': 'Book added successfully'})

# updating the book using put request
@app.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    bookslist = read_file_csv()
    for book in bookslist:
        if book['id'] == book_id:
            book['title'] = request.json.get('title')
            book['author'] = request.json.get('author')
            book['gener'] = request.json.get('gener')
            book['publication_year'] = request.json.get('publication_year')
            write_file_csv(bookslist)
            return jsonify({'message': 'book updated successfully'})
    return jsonify({'message': 'book with given ID is not found'}), 404

# Deleting a particular record with given ID
@app.route('/books/<string:book_id>', methods=['DELETE'])
def delete_store(book_id):
    bookslist = read_file_csv()
    for book in bookslist:
        if book['id'] == book_id:
            bookslist.remove(book)
            write_file_csv(bookslist)
            return jsonify({'message': 'book with that ID deleted successfully'})
    return jsonify({'message': 'Book with given ID Not Found'})


#searching the given book with name or gener or publicatio year
@app.route('/searchbook/<string:word>',methods=['GET'])
def search_books(word):
    bookslist=read_file_csv()
    result=[]
    for book in bookslist:
        if((book['title'] == word) or (book['gener'] == word) or (book['author']== word) or (book['publication_year'] == word)):
            result.append(book)  #appedning in list to display if more than one book exists 
    if len(result) != 0:
        return(result)
    else:
        return({'message':'No book found Found'})


#Running the application using run method
if __name__ == '__main__':
    app.run(debug=True)