from models import Author, Book, Customer, Order, OrderItem, session


#find All Book:
def getAllBooks():
    books = session.query(Book.id, Book.title, Author.name, Book.genre ).join(Author, Book.author_id==Author.id).all()
    for book in books:
        print(f"Id: {book.id}, Title: {book.title}, Author: {book.name}, Genre:  {book.genre}")

#Find All authors with all book
def getAllAuthors():
    authors=session.query(Author).all()
    for author in authors: 
        print(f"ID: {author.id}, Name: {author.name}, Country: {author.country}")
        
def getAllAuthorsWithBooks():
    authors=session.query(Author, Book.title).join(Book, Author.id==Book.author_id).all()    
    for author in authors: 
        print(f"ID: {author.Author.id}, Name: {author.Author.name}, Books: {author.title}")

def getBooksByauthor(author):
    books=session.query(Book.id, Book.title, Author.name, Book.genre ).join(Author, Book.author_id==Author.id).filter(Author.name==author).all()
    for book in books:
        print(f"Id: {book.id}, Title: {book.title}, Author: {book.name}, Genre:  {book.genre}")

def getBooksByGenre(genre):
    books=session.query(Book.id, Book.title, Author.name, Book.genre ).join(Author, Book.author_id==Author.id).filter(Book.genre==genre).all()
    for book in books:
        print(f"Id: {book.id}, Title: {book.title}, Author: {book.name}, Genre:  {book.genre}")

def getBooksById(id):
    book=session.query(Book.id, Book.title, Author.name, Book.genre ).join(Author, Book.author_id==Author.id).filter(Book.id==id).first()
    print(f"Id: {book.id}, Title: {book.title}, Author: {book.name}, Genre:  {book.genre}")
    return book

def getAllCustomers():
    customers=session.query(Customer).all()
    for customer in customers:
        print(f"ID: {customer.id}, Name: {customer.name}, Email: : {customer.email},  ")
        #Ordered Books: {[[item.book.title, item.quantity] for order in customer.orders for item in order.items]}

        
def getOrderedBooksOfCustomers(id):
    customer=session.query(Customer).filter(Customer.id==id).first()
    print(f"Name: {customer.name}, Email: : {customer.email}, Order Id: {[order.id for order in customer.orders]}Ordered Books: {[[item.book.title, item.quantity] for order in customer.orders for item in order.items]} ")
    for order in customer.orders:
        print('Order id: ',order.id )
        for item in order.items:
 bfdbfdhfhjhhhfdhfdhfdhfdhhfhhhhhhfhfhfhfhfhbbbbbbbvb            print(f"Book: {item.book.title}, Quantity: {item.quantity}: price: {item.quantity*item.book.price}")
        print(f"Total price: {order.total_amount}") 

    


print("\nAll Books with Authors")
getAllBooks()
print('\nAll Authors')
getAllAuthors()
print('\nAll Authors with their Books')
getAllAuthorsWithBooks()

print("All books by specific Authors")
getBooksByauthor('J.K. Rowling')

print("All books by specific Genre")
getBooksByGenre('Mystery')

print("book by specific id")
getBooksById(18)

print("All customers:")
getAllCustomers()
print("Book of Customers")
getOrderedBooksOfCustomers(3)**********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************8
