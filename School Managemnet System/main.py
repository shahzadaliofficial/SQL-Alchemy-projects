from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from menu import menu

engine = create_engine('sqlite:///school.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def initialize_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    # Import and generate sample data
    from sample_data import generate_sample_data
    generate_sample_data(session)

if __name__ == "__main__":
    initialize_db()
    menu(session)