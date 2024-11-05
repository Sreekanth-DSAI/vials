"""
Explanation of the Code:

1. This script connects to a PostgreSQL database to manage user accounts.
2. Uses SQLAlchemy for database interactions and defines a session for database access.
3. Functions to create users, authenticate users, and send password emails are implemented.
4. Passwords are securely hashed using Werkzeug's security utilities.
5. Integrity errors are handled to prevent duplicate user entries.
6. Streamlit is used for session management, specifically for storing user information.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText
import smtplib
import random
import string
from datetime import datetime
from models import User, Base
from sqlalchemy.exc import IntegrityError  # Import to handle IntegrityError
import streamlit as st

# Database setup
DATABASE_URL = "postgresql://dbmasteruser:<lmFpK}PF4u$je+][w=:h4~_!Zz%It]J@ls-8a62cbf5a61df28a063d1a9329e3104b75eefab3.chvkci9uhgu1.ap-south-1.rds.amazonaws.com/Vials"
engine = create_engine(DATABASE_URL)  # Create a database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Create a session factory
Base.metadata.create_all(bind=engine)  # Create database tables

def get_db():
    """
    Provides a database session for use in the application.

    Returns:
        Session: A new SQLAlchemy session.
    """
    return SessionLocal()

# Admin functions for managing users
def create_user(db, employee_id, first_name, last_name, email, mobile_contact):
    """
    Creates a new user in the database.

    Parameters:
    db (Session): The database session.
    employee_id (str): The employee ID of the new user.
    first_name (str): The first name of the new user.
    last_name (str): The last name of the new user.
    email (str): The email of the new user.
    mobile_contact (str): The mobile contact of the new user.

    Returns:
    User: The created user object or None if creation failed.
    """
    password = generate_random_password()  # Generate a random password
    hashed_password = generate_password_hash(password)  # Hash the password

    user = User(
        employee_id=employee_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        mobile_contact=mobile_contact,
        hashed_password=hashed_password
    )
    
    try:
        db.add(user)  # Add the user to the session
        db.commit()  # Commit the transaction

        # Send the password email after committing the user
        send_password_email(email, password)  # Send email with password
        
        return user  # Return the created user
    
    except IntegrityError as e:  # Handle integrity errors
        db.rollback()  # Rollback the transaction if there is an error
        if "duplicate key value violates unique constraint" in str(e):
            print("Error: User with this email already exists.")
        else:
            print(f"Error creating user: {str(e)}")

def create_test_user():
    """
    Creates a test user for development purposes.

    Returns:
    User: The created test user object or None if creation failed.
    """
    db = get_db()  # Get a database session
    email = "testuser@example.com"  # Test user email
    password = "testpassword"  # Test password
    hashed_password = generate_password_hash(password)  # Hash the test password
    
    # Check if the test user already exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            employee_id="TEST123",
            first_name="Test",
            last_name="User",
            email=email,
            mobile_contact="1234567890",
            hashed_password=hashed_password
        )
        try:
            db.add(user)  # Add the user to the session
            db.commit()  # Commit the transaction
            send_password_email(email, password)  # Send email with password
            return user  # Return the created user
        
        except IntegrityError as e:  # Handle integrity errors
            db.rollback()  # Rollback the transaction
            if "duplicate key value violates unique constraint" in str(e):
                print("Error: User with this email already exists.")
            else:
                print(f"Error creating user: {str(e)}")

def generate_random_password(length=8):
    """
    Generates a random password.

    Parameters:
    length (int): The length of the password to generate (default is 8).

    Returns:
    str: The generated random password.
    """
    characters = string.ascii_letters + string.digits  # Characters used for password generation
    password = ''.join(random.choice(characters) for _ in range(length))  # Create a random password
    return password

def send_password_email(email, password):
    """
    Sends an email with the user's password.

    Parameters:
    email (str): The email address of the recipient.
    password (str): The password to be sent in the email.

    Returns:
    None
    """
    sender_email = "putsalasreekanth@gmail.com"  # Sender's email
    sender_password = "mlekzgpvtcgulocp"  # Sender's email password
    subject = "Your Account Password"  # Email subject
    body = f"Your account has been created. Your login password is: {password}"  # Email body

    msg = MIMEText(body)  # Create the email message
    msg["Subject"] = subject  # Set the subject
    msg["From"] = sender_email  # Set the sender
    msg["To"] = email  # Set the recipient

    with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Set up the SMTP server
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)  # Log in to the server
        server.sendmail(sender_email, email, msg.as_string())  # Send the email

def authenticate(email, password):
    """
    Authenticates a user based on email and password.

    Parameters:
    email (str): The user's email.
    password (str): The user's password.

    Returns:
    User: The authenticated user object or None if authentication fails.
    """
    db = get_db()  # Get a database session
    user = db.query(User).filter(User.email == email).first()  # Query the user by email
    if user and check_password_hash(user.hashed_password, password):  # Check password
        st.session_state["username"] = f"{user.first_name} {user.last_name}"  # Store username in session
        return user  # Return the authenticated user
    return None  # Return None if authentication fails
