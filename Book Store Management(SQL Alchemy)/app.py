from models import Author, Book, Customer, Order, OrderItem, session

# Adding sample data for authors
authors = [
    Author(name="J.K. Rowling", country="United Kingdom"),
    Author(name="George R.R. Martin", country="United States"),
    Author(name="J.R.R. Tolkien", country="United Kingdom"),
    Author(name="Agatha Christie", country="United Kingdom"),
    Author(name="Dan Brown", country="United States")
]

# Adding sample data for books
books = [
    Book(title="Harry Potter and the Philosopher's Stone", author=authors[0], genre="Fantasy", price=20.0, stock_quantity=100),
    Book(title="Harry Potter and the Chamber of Secrets", author=authors[0], genre="Fantasy", price=22.0, stock_quantity=90),
    Book(title="Harry Potter and the Prisoner of Azkaban", author=authors[0], genre="Fantasy", price=23.0, stock_quantity=80),
    Book(title="A Game of Thrones", author=authors[1], genre="Fantasy", price=25.0, stock_quantity=50),
    Book(title="A Clash of Kings", author=authors[1], genre="Fantasy", price=26.0, stock_quantity=45),
    Book(title="A Storm of Swords", author=authors[1], genre="Fantasy", price=28.0, stock_quantity=40),
    Book(title="The Hobbit", author=authors[2], genre="Fantasy", price=15.0, stock_quantity=80),
    Book(title="The Fellowship of the Ring", author=authors[2], genre="Fantasy", price=18.0, stock_quantity=75),
    Book(title="The Two Towers", author=authors[2], genre="Fantasy", price=19.0, stock_quantity=70),
    Book(title="The Return of the King", author=authors[2], genre="Fantasy", price=20.0, stock_quantity=65),
    Book(title="Murder on the Orient Express", author=authors[3], genre="Mystery", price=10.0, stock_quantity=100),
    Book(title="And Then There Were None", author=authors[3], genre="Mystery", price=12.0, stock_quantity=90),
    Book(title="The Da Vinci Code", author=authors[4], genre="Thriller", price=15.0, stock_quantity=80),
    Book(title="Angels & Demons", author=authors[4], genre="Thriller", price=16.0, stock_quantity=75),
    Book(title="Inferno", author=authors[4], genre="Thriller", price=17.0, stock_quantity=70),
    Book(title="Deception Point", author=authors[4], genre="Thriller", price=18.0, stock_quantity=65),
    Book(title="Digital Fortress", author=authors[4], genre="Thriller", price=14.0, stock_quantity=60),
    Book(title="The Pale Horse", author=authors[3], genre="Mystery", price=9.0, stock_quantity=95),
    Book(title="Death on the Nile", author=authors[3], genre="Mystery", price=11.0, stock_quantity=85),
    Book(title="Curtain", author=authors[3], genre="Mystery", price=13.0, stock_quantity=80)
]

# Adding sample data for customers
customers = [
    Customer(name="Alice Smith", email="alice@example.com"),
    Customer(name="Bob Johnson", email="bob@example.com"),
    Customer(name="Charlie Brown", email="charlie@example.com"),
    Customer(name="David Wilson", email="david@example.com"),
    Customer(name="Emily Davis", email="emily@example.com")
]
session.add_all(authors + books + customers)
session.commit()
# Adding sample orders and order items
# Adding orders with items using the items relationship
orders = [
    Order(
        customer=customers[0],
        items=[
            OrderItem(book=books[0], quantity=2),
            OrderItem(book=books[1], quantity=1),
        ]
    ),
    Order(
        customer=customers[1],
        items=[
            OrderItem(book=books[3], quantity=3),
        ]
    ),
    Order(
        customer=customers[2],
        items=[
            OrderItem(book=books[5], quantity=2),
            OrderItem(book=books[7], quantity=1),
        ]
    ),
    Order(
        customer=customers[3],
        items=[
            OrderItem(book=books[10], quantity=4),
            OrderItem(book=books[11], quantity=2),
        ]
    ),
    Order(
        customer=customers[4],
        items=[
            OrderItem(book=books[14], quantity=5),
            OrderItem(book=books[18], quantity=3),
        ]
    )
]


# Then add orders
for order in orders:
    session.add(order)
    session.commit()

# Commit changes to the database


print("Orders with items added successfully!")

'''
order_items = [
    OrderItem(order=orders[0], book=books[0], quantity=2),
    OrderItem(order=orders[0], book=books[1], quantity=1),
    OrderItem(order=orders[1], book=books[3], quantity=3),
    OrderItem(order=orders[2], book=books[5], quantity=2),
    OrderItem(order=orders[2], book=books[7], quantity=1),
    OrderItem(order=orders[3], book=books[10], quantity=4),
    OrderItem(order=orders[3], book=books[11], quantity=2),
    OrderItem(order=orders[4], book=books[14], quantity=5),
    OrderItem(order=orders[4], book=books[18], quantity=3)
]

# Adding all data to session

# Commit changes to the database
session.commit()

# Verifying the data
print("Extended sample data added successfully!")
'''
