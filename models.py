import datetime
from decimal import Decimal
from pydantic import BaseModel
from sqlalchemy import DECIMAL, CheckConstraint, Column, Date, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# This function is used to define models(tables) in database which are class in python code to achieve ORM - Object Relationshup Management
Base = declarative_base()

# Defining Customer model
class Customer(Base):
    __tablename__ = "customers"

    customerid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    loyalty_points = Column(Integer)

    # Defining relation with Rental table
    child_rental = relationship('Rental', back_populates='customer')

class Movie(Base):
    __tablename__ = "movies"

    movieid = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String)
    availability = Column(Boolean, default=True)
    
    # Defining relation with Rental table
    child_rental = relationship('Rental', back_populates='movie')

    
class Rental(Base):
    __tablename__ = "rentals"

    rentalid = Column(Integer, primary_key=True, index=True)
    customerid = Column(Integer, ForeignKey('customers.customerid'))
    movieid = Column(Integer, ForeignKey('movies.movieid'))
    rental_date = Column(Date,default= datetime.date.today)
    due_date = Column(Date)
    return_date  = Column(Date)
    status = Column(String(20), CheckConstraint("status IN ('rented','returned')",name='status_check'))

    # Defining relation with customer table
    customer = relationship('Customer', back_populates='child_rental')
    # Defining relation with movie table
    movie = relationship('Movie', back_populates='child_rental')
    # Defining relation with Rental table
    child_payment = relationship('Payment', back_populates='rental')

class Payment(Base):
    __tablename__ = "payments"

    paymentid = Column(Integer, primary_key=True, index=True)
    rentalid = Column(Integer, ForeignKey('rentals.rentalid'))
    amount = Column(DECIMAL(10,2))
    payment_date = Column(Date, default=datetime.date.today)

    # Defining relation with rental table
    rental = relationship('Rental', back_populates='child_payment')



# Pydantic Models to validate input data
class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    loyalty_points: int

class MovieCreate(BaseModel):
    title: str
    category: str
    availability: bool

class RentalCreate(BaseModel):
    customerid : int
    movieid : int
    rental_date: datetime.date
    due_date: datetime.date
    return_date : datetime.date
    status: str

class PaymentCreate(BaseModel):
    rentalid: int
    amount: Decimal
    payment_date: datetime.date
    
