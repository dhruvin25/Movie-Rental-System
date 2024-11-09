from datetime import date
import json
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import psycopg2
import models as md


# Getting Credentials from config.json
def load_db_config(file_path):
    try:
        with open(file_path,'r') as fp:
            config = json.load(fp)
        return config
    except Exception as error:
        print(f"Error loading database configuration: {error}")
        return None

file_path = "config.json"
config = load_db_config(file_path)

try:
    config = load_db_config(file_path)
    if config:
        db_name = config["db_name"]
        user = config["user"]
        password = config["password"]
        host = config["host"]
        port = config["port"]     
        # Database Connection Settings
        DATABASE_URL= f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

except Exception as error:
    print(error)


# Creating a FastAPI Instance
app = FastAPI()  # Move the app outside the main function


# Set up the Database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)   # Manages Database Session 
Base = declarative_base()

Base.metadata.create_all(bind=engine)

# Dependency function to create database session for each request and ensures that session is closed after handling request.
def get_db():
    db = SessionLocal()
    try:
        yield db    # This allows the session to be used during request and close it after the request is handled.
    finally: 
        db.close()

# End-point to add Customer 
@app.post("/customer_add/")
def create_customer(customer: md.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = md.Customer(name=customer.name, email=customer.email,phone = customer.phone , loyalty_points=customer.loyalty_points)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# End-point to get Customers
@app.get("/customers/")
def get_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    customers = db.query(md.Customer).offset(skip).limit(limit).all()
    return customers

# End-point to add movie
@app.post("/movie_add/")
def create_movie(movie: md.MovieCreate, db: Session = Depends(get_db)):
    db_movie = md.Movie(title=movie.title, category=movie.category, availability=movie.availability)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# End-point to get Movies
@app.get("/movies/")
def get_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = db.query(md.Movie).offset(skip).limit(limit).all()
    return movies

# End-point to add Rental
@app.post("/rental_add/")
def create_rental(rental: md.RentalCreate, db: Session = Depends(get_db)):
    db_rental = md.Rental(customerid=rental.customerid, movieid=rental.movieid, rental_date=rental.rental_date, due_date=rental.due_date, return_date=rental.return_date, status=rental.status)
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    return db_rental

# End-point to get Rentals
@app.get("/rentals/")
def get_rentals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rentals = db.query(md.Rental).offset(skip).limit(limit).all()
    return rentals

# End-point to add payment 
@app.post("/payment_add/")
def create_payment(payment: md.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = md.Payment(rentalid=payment.rentalid, amount=payment.amount, payment_date=payment.payment_date)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

# End-point to get payments
@app.get("/payments/")
def get_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    payments = db.query(md.Payment).offset(skip).limit(limit).all()
    return payments


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
