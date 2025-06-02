from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import datetime
from sqlalchemy.event import listen




db_url="sqlite:///bookstore.db"

engine=create_engine(db_url)

Base=declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    books = relationship('Book', back_populates='author')



class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    genre = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)

    author = relationship('Author', back_populates='books')
    # def __repr__(self):
    #     return f"Book(Id: {self.id}, Title: {self.title}, Genre: {self.genre}, Author: {self.author.name}"

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    orders = relationship('Order', back_populates='customer')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float, default=0.0)
    
    customer = relationship("Customer", back_populates="orders")
    items = relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationships
    order = relationship('Order', back_populates='items')
    book = relationship('Book')

Base.metadata.create_all(engine)

#Events:
def calculates_order_total(mapper, connection, target):
    session = Session.object_session(target)
    if session is not None:
        order = session.query(Order).get(target.order_id)
        if order:
            total = sum(item.quantity * item.book.price for item in order.items)
            connection.execute(
                Order.__table__.update().
                where(Order.__table__.c.id == target.order_id).
                values(total_amount=total)
            )

def books_stock_manage(mapper, connection, target):
    session = Session.object_session(target)
    if session is not None:
        book = session.query(Book).get(target.book_id)
        if book:
            if book.stock_quantity >= target.quantity:
                connection.execute(
                    Book.__table__.update().
                    where(Book.__table__.c.id == target.book_id).
                    values(stock_quantity=book.stock_quantity - target.quantity)
                )
            else:
                raise ValueError(f"Not enough stock available for the book: {book.title}")
#Listen
listen(OrderItem, "after_insert", calculates_order_total)
listen(OrderItem, "after_update", calculates_order_total)
listen(OrderItem, "after_delete", calculates_order_total)
listen(OrderItem, "before_insert", books_stock_manage)



Session=sessionmaker(bind=engine)
session=Session()
