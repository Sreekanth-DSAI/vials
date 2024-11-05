"""
Explanation of the Code:

1. This code defines the SQLAlchemy ORM (Object Relational Mapping) models used to interact with a relational database.
2. Two models are defined:
    - `User`: Represents user information such as employee details, contact, and password management fields.
    - `DetectionData`: Stores data related to image detections, including counts of PFS (Pre-filled Syringes) and vials.
3. The `Base` object is created using `declarative_base()` which serves as a base class for the models.
4. The models map Python classes to database tables and define columns corresponding to the fields in each table:
    - The `User` model has fields like `employee_id`, `email`, and `hashed_password` to store user credentials and contact details.
    - The `DetectionData` model contains fields such as `image_name`, `model_name`, `pfs_count`, `vial_count`, and `timestamp` for storing information about image detection results.
5. Default values and constraints are provided for certain columns:
    - `last_password_change` and `timestamp` default to the current UTC time using `datetime.utcnow`.
    - Unique constraints are enforced on fields such as `employee_id` and `email` in the `User` model to ensure no duplicates.
6. Indexes are defined on fields like `employee_id`, `email`, and `image_name` for faster querying.
7. These models will be used to perform database operations like creating, reading, updating, and deleting user and detection data.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create the base class for declarative class definitions
Base = declarative_base()

# Define the User model
class User(Base):
    """
    ORM model representing a user in the database.

    Columns:
    - id: Primary key, unique identifier for each user.
    - employee_id: Unique employee ID, indexed for faster queries.
    - first_name: First name of the user.
    - last_name: Last name of the user.
    - email: User's email address, must be unique.
    - mobile_contact: Contact number for the user.
    - hashed_password: Securely hashed user password.
    - last_password_change: Timestamp of the last password change, defaults to current UTC time.
    - password_reset_token: Token used for password reset, nullable.
    - password_reset_token_expiry: Expiry timestamp for the password reset token, nullable.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    mobile_contact = Column(String(15))
    hashed_password = Column(String(200))
    last_password_change = Column(DateTime, default=datetime.utcnow)
    password_reset_token = Column(String(100), nullable=True)
    password_reset_token_expiry = Column(DateTime, nullable=True)

# Define the DetectionData model
class DetectionData(Base):
    """
    ORM model representing image detection data in the database.

    Columns:
    - id: Primary key, unique identifier for each detection record.
    - image_name: Name of the image file associated with the detection, indexed.
    - model_name: Name of the model used for detection, indexed.
    - pfs_count: Number of pre-filled syringes (PFS) detected in the image.
    - vial_count: Number of vials detected in the image.
    - timestamp: Timestamp when the detection was made, defaults to current UTC time.
    """
    __tablename__ = "detection_data"
    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String(100), index=True)
    model_name = Column(String(100), index=True)
    pfs_count = Column(Integer, default=0)
    vial_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
