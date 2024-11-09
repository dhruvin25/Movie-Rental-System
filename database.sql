-- Database name = movie_rental_system

-- Create Customers table
create table Customers(
	customerid SERIAL PRIMARY KEY,
	name VARCHAR(100),
	email VARCHAR(100) UNIQUE,
	phone VARCHAR(15),
	loyalty_points INTEGER DEFAULT 0
);

-- Create Movies table
create table Movies(
	movieid SERIAL PRIMARY KEY,
	title VARCHAR(150),
	category VARCHAR(50),
	availability BOOLEAN DEFAULT TRUE
);

-- Create Rentals table
create table Rentals(
	rentalid SERIAL PRIMARY KEY,
	customerid INT REFERENCES Customers(customerid),
	movieid INT REFERENCES Movies(movieid),
	rental_date DATE DEFAULT CURRENT_DATE,
	due_date DATE,
	return_date DATE,
	status VARCHAR(20) CHECK (status IN ('rented','returned'))
);

-- Create Payments table
CREATE TABLE Payments(
	paymentsid SERIAL PRIMARY KEY,
	rentalid INT REFERENCES Rentals(rentalid),
	payment_date DATE DEFAULT CURRENT_DATE,
	amount DECIMAL(10,2)
);

-- Stores Procedure to calculate late fees
CREATE OR REPLACE PROCEDURE calculate_late_fees(IN rentalID_input INT)
LANGUAGE plpgsql
AS $$
DECLARE 
	fee_per_day DECIMAL := 5.00;
	days_late INT;
BEGIN 
	SELECT (return_date - due_date) INTO days_late FROM Rentals WHERE rentalID = rentalID_input;
	IF days_late > 0 THEN
		INSERT INTO Payments(rentalID, payment_date, amount)
		VALUES (rentalID_input, CURRENT_DATE, days_late* fee_per_day);
	END IF;
END;
$$;

-- Trigger for automatic record Deletion 
CREATE OR REPLACE FUNCTION delete_related_records() RETURNS TRIGGER AS $$
BEGIN 
	DELETE FROM Payments WHERE rentalID IN (SELECT rentalID FROM Rentals WHERE customerid = OLD.customerid);
	DELETE FROM Rentals WHERE customerid = OLD.customerid;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER customer_delete_trigger
	BEFORE DELETE ON Customers
	FOR EACH ROW
	EXECUTE FUNCTION delete_related_records();
-- drop trigger customer_delete_trigger on Customers;
DELETE FROM Customers WHERE customerid = 1;
-- Inserting Customer
INSERT INTO Customers (name, email, phone, loyalty_points)
VALUES ('John Doe', 'john.doe@gmail.com', '1234567890', 100);
SELECT * FROM Customers;

-- Insert Movie
INSERT INTO Movies (title, category, availability)
VALUES ('The Matrix', 'Sci-FI', TRUE),('Inception', 'Action', TRUE);
SELECT * FROM Movies;

-- Adding Rental
INSERT INTO Rentals (customerid, movieid, due_date, status)
VALUES (1, 1, CURRENT_DATE + INTERVAL '7 days', 'rented');
select * from Rentals;

-- Updating return date
UPDATE Rentals 
SET return_date = CURRENT_DATE + INTERVAL '12 days', status = 'returned'
WHERE rentalID = 1;
SELECT * FROM Rentals;

-- Calling Procedure "calculate_late_fees" for customerid = 1
CALL calculate_late_fees(1);
SELECT * FROM Payments;

-- DELETE FROM Customers WHERE customerid = 1;
-- This will give error because customerid table is referenced in Rentals table.

INSERT INTO Rentals (customerid, movieid, rental_date, due_date, return_date)
VALUES (1, 2, '2024-01-01', '2024-01-05', '2024-01-06');
SELECT * FROM Rentals;


INSERT INTO Payments (rentalID, payment_date, amount)
VALUES (1, '2024-01-06',5.00), (2, '2024-01-10', 10.00);
SELECT * FROM PAYMENTS;






-- First delete related records in Payments table
DELETE FROM Payments WHERE rentalID IN (SELECT rentalID FROM Rentals WHERE customerid = 1);

-- Then delete related records in Rentals table
DELETE FROM Rentals WHERE customerid = 1;

-- Now you can safely delete the customer
DELETE FROM Customers WHERE customerid = 1;


drop table Customers, movies, rentals, payments;