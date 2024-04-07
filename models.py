# Import necessary modules
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize MetaData
metadata = MetaData()

# Define Favourites model
class Favourites(db.Model):
    __tablename__ = 'favourites'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # User ID
    board_id = db.Column(db.Integer, db.ForeignKey('boards.board_id'), primary_key=True)  # Board ID

# Define User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # Define properties for flask_login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True 

    @property
    def is_anonymous(self):
        return False

    # Define method to get user id
    def get_id(self):
        return str(self.id)
    
    # Define columns for User table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    bio = db.Column(db.Text)
    user_password = db.Column(db.Text, nullable=False)
    user_boards = db.relationship('Board', backref='user', lazy=True)
    favourite_boards = db.relationship('Board', secondary='favourites', backref=db.backref('favourited_by', lazy='dynamic'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Define class method to sign up a user
    @classmethod
    def signup(cls, username, email, password, image_url, bio):
        hashed_pwd = generate_password_hash(password)  # Hash the password

        # Create a new user
        user = User(
            username=username,
            email=email,
            image_url=image_url,
            bio=bio,
            user_password=hashed_pwd
        )

        db.session.add(user)  # Add the user to the session
        return user  # Return the user

    # Define class method to authenticate a user
    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()  # Get the user

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.user_password, password):
            return user  # Return the user

        return False  # Return False if the user does not exist or the password is incorrect
class Board(db.Model):
    __tablename__ = 'boards'  # Define the table name

    # Define the columns for the table 'boards'
    board_id = db.Column(db.Integer, primary_key=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key referencing 'users' table
    asking_price = db.Column(db.DECIMAL)
    board_manufacturer = db.Column(db.String(255))
    board_length_feet = db.Column(db.Integer)
    board_length_inches = db.Column(db.Integer)
    board_length_total = db.Column(db.Integer)
    condition = db.Column(db.String(50))
    sell_or_rent = db.Column(db.String(20))
    board_location = db.Column(db.String(255))
    delivery_options = db.Column(db.String(50))
    model = db.Column(db.String(255))
    width_integer = db.Column(db.Integer)
    width_fraction = db.Column(db.String(5))
    width_total = db.Column(db.Float)
    depth_integer = db.Column(db.Integer)
    depth_fraction = db.Column(db.String(5))
    depth_total = db.Column(db.Float)
    volume_litres = db.Column(db.Integer)
    extra_details = db.Column(db.String(255))
    main_photo = db.Column(db.Text)  # Main photo URL
    extra_photos = db.Column(JSON)  # Extra photos URLs, stored as a list
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())  # Default to current timestamp
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())  # Update to current timestamp when the record is updated
    

class Message(db.Model):
    __tablename__ = 'messages'  # Define the table name

    # Define the columns for the table 'messages'
    message_id = db.Column(db.Integer, primary_key=True)  # Primary key
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key referencing 'users' table
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key referencing 'users' table
    board_id = db.Column(db.Integer, db.ForeignKey('boards.board_id'))  # Foreign key referencing 'boards' table
    message_content = db.Column(db.TEXT)
    sent_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())  # Default to current timestamp

class SearchPreference(db.Model):
    __tablename__ = 'search_preferences'  # Define the table name

    # Define the columns for the table 'search_preferences'
    search_id = db.Column(db.Integer, primary_key=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key referencing 'users' table
    board_type = db.Column(db.String(255))
    condition = db.Column(db.String(50))
    board_location = db.Column(db.String(255))
    max_price = db.Column(db.DECIMAL(10, 2))
    min_price = db.Column(db.DECIMAL(10, 2))
    board_manufacturer = db.Column(db.String(255))
    board_length_feet = db.Column(db.Integer)
    board_length_inches = db.Column(db.Integer)
    min_length = db.Column(db.Integer)
    max_length = db.Column(db.Integer)
    board_length_total = db.Column(db.Integer)
    sell_or_rent = db.Column(db.String(20))
    model = db.Column(db.String(255))
    width_integer = db.Column(db.Integer)
    width_fraction = db.Column(db.String(5))
    min_width = db.Column(db.DECIMAL(10, 2))
    max_width = db.Column(db.DECIMAL(10, 2))
    width_total = db.Column(db.DECIMAL(10, 2))
    depth_integer = db.Column(db.Integer)
    depth_fraction = db.Column(db.String(5))
    min_depth = db.Column(db.DECIMAL(10, 2))
    max_depth = db.Column(db.DECIMAL(10, 2))
    depth_total = db.Column(db.DECIMAL(10, 2))
    volume_litres = db.Column(db.Integer)
    min_volume = db.Column(db.Integer)
    max_volume = db.Column(db.Integer)
    main_photo = db.Column(db.Text)  # Main photo URL
    extra_photos = db.Column(JSON)  # Extra photos URLs, stored as a list
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())  # Default to current timestamp
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())  # Update to current timestamp when the record is updated