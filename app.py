from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Board, Message, SearchPreference, Favourites
from forms import UserAddForm, LoginForm, BoardForm, SearchForm
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
from flask_login import current_user, LoginManager, login_user, logout_user, login_required 
from flask import Flask, request
from google.cloud import storage
import uuid
import math
import os

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/my_service_account_key.json'
MAPBOX_API_KEY = 'pk.eyJ1IjoidGhvbWV3b29kIiwiYSI6ImNsdXBueWs5ejA2NHoyanBiM3h5MTFiZjQifQ.6lwwE00ZXTxf8XBXUeCDew'

login_manager = LoginManager()

def upload_blob(file_object, destination_blob_name=None):
    """Uploads a file to the bucket."""
    bucket_name = "board-market"  # Update with your bucket name
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # If destination_blob_name is empty, generate a unique name using a UUID
    if not destination_blob_name:
        destination_blob_name = str(uuid.uuid4())

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(file_object)

    print(f"File uploaded to {destination_blob_name}.")

def download_blob(source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    bucket_name = "board-market"  # Update with your bucket name
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def create_app():
    print("Creating app...")
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    login_manager.init_app(app)
    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour in seconds
    
    app.config['SECRET_KEY'] = 'secret'
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///boardmarket'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['SQLALCHEMY_ECHO'] = True
    app.debug = True
    db.init_app(app)
    print("App created successfully.")

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)
    
    @app.context_processor
    def inject_mapbox_api_key():
        return dict(MAPBOX_API_KEY=MAPBOX_API_KEY)
    
    # This function applies filters to a query based on the form data
    def apply_filters(query, form):
        # Print the form data for debugging purposes
        print(f"Form data in apply_filters: {form.data}")
        
        # If both min_price and max_price are provided, filter the query by price
        if form.min_price.data is not None and form.max_price.data is not None:
            min_price = form.min_price.data
            max_price = form.max_price.data
            if min_price > 0:
                query = query.filter(Board.asking_price.between(min_price, max_price))
            else:
                query = query.filter(Board.asking_price <= max_price)

        # If board_manufacturer is provided, filter the query by board_manufacturer
        if form.board_manufacturer.data:
            query = query.filter(Board.board_manufacturer.ilike(f"%{form.board_manufacturer.data}%"))

        # If both min_length and max_length are provided, filter the query by length
        if form.min_length.data is not None and form.max_length.data is not None:
            min_length = form.min_length.data
            max_length = form.max_length.data
            query = query.filter(Board.board_length_total.between(min_length, max_length))

        # If condition is provided, filter the query by condition
        if form.condition.data:
            query = query.filter(Board.condition.ilike(f"%{form.condition.data}%"))

        # If sell_or_rent is provided, filter the query by sell_or_rent
        if form.sell_or_rent.data:
            query = query.filter(Board.sell_or_rent.ilike(f"%{form.sell_or_rent.data}%"))

        # If board_location is provided, filter the query by board_location
        if form.board_location.data:
            query = query.filter(Board.board_location.ilike(f"%{form.board_location.data}%"))

        # If delivery_options is provided, filter the query by delivery_options
        if form.delivery_options.data:
            query = query.filter(Board.delivery_options.ilike(f"%{form.delivery_options.data}%"))

        # If model is provided, filter the query by model
        if form.model.data:
            query = query.filter(Board.model.ilike(f"%{form.model.data}%"))

        # If width_integer or width_fraction is provided, filter the query by width
        if form.width_integer.data is not None or form.width_fraction.data is not None:
            total_width = form.width_integer.data if form.width_integer.data else 0
            total_width += fraction_to_decimal(form.width_fraction.data) if form.width_fraction.data else 0
            if total_width > 0:
                query = query.filter(Board.width_total <= total_width)

        # If both min_depth and max_depth are provided, filter the query by depth
        if form.min_depth.data is not None and form.max_depth.data is not None:
            min_depth = float(form.min_depth.data)
            max_depth = float(form.max_depth.data)
            if min_depth >= 0 and max_depth >= min_depth:
                query = query.filter(Board.depth_total.between(min_depth, max_depth))

        # If both min_volume and max_volume are provided, filter the query by volume
        if form.min_volume.data is not None and form.max_volume.data is not None:
            min_volume = form.min_volume.data
            max_volume = form.max_volume.data
            if min_volume >= 0 and max_volume >= min_volume:
                query = query.filter(Board.volume_litres.between(min_volume, max_volume))

        # Return the filtered query
        return query

    # This function converts a fraction to a decimal
    def fraction_to_decimal(fraction):
        if fraction == '':
            return None
        numerator, denominator = map(int, fraction.split('/'))
        return numerator / denominator

    # This function converts feet to inches
    def convert_feet_to_inches(feet):
        if feet is None:
            return 0
        inches = feet * 12
        return inches

    # This function converts inches to feet and inches
    def convert_inches_to_feet(inches):
        feet = inches // 12
        remaining_inches = inches % 12
        return f"{feet}' {remaining_inches}\""

    def convert_decimal_to_fraction(value):
        try:
            value = float(value)
        except ValueError:
            return ''

        numerator = round(value * 16)
        denominator = 16

        if numerator == 0:
            return ''

        # Simplify the fraction
        gcd = math.gcd(numerator, denominator)
        numerator //= gcd
        denominator //= gcd

        return str(numerator) + ('' if denominator == 1 else '/' + str(denominator)) + '"'

    @app.template_filter('type')
    def type_filter(value):
        return str(type(value))

    # This route serves the home page
    @app.route('/')
    def index():
        user_id = current_user.id if current_user.is_authenticated else None
        return render_template('index.html')

    @app.route('/signup', methods=["GET", "POST"])
    def signup():
        """Handle user signup."""

        form = UserAddForm()

        if form.validate_on_submit():
            print("Form validated")  # Debugging line
            try:
                # Get the file from the form
                image_file = request.files['image_file']
                filename = secure_filename(image_file.filename)
                print(f"Image file: {filename}")  # Debugging line

                # Upload the file to Google Cloud Storage
                upload_blob(image_file, filename)

                # Get the URL of the uploaded file
                image_url = f"https://storage.googleapis.com/board-market/{filename}"
                print(f"Image URL: {image_url}")  # Debugging line

                user = User.signup(
                    username=form.username.data,
                    password=form.password.data,
                    email=form.email.data,
                    image_url=image_url,
                    bio=form.bio.data
                )
                print("User signed up")  # Debugging line

                db.session.commit()
                print("Database commit successful")  # Debugging line

            except IntegrityError:
                print("IntegrityError occurred")  # Debugging line
                flash("Username already taken", 'danger')
                return render_template('users/signup.html', form=form)

            login_user(user)  # Use flask_login's login_user function
            print("User logged in")  # Debugging line

            return redirect("/")

        else:
            print(form.errors)  # print form errors if validation fails

        return render_template('users/signup.html', form=form)


    @app.route('/login', methods=["GET", "POST"])
    def login():
        """Handle user login."""

        form = LoginForm()

        if form.validate_on_submit():
            user = User.authenticate(form.username.data,
                                    form.password.data)

            if user:
                login_user(user)  # Use flask_login's login_user function
                flash(f"Hello, {user.username}!", "success")
                return redirect("/")

            flash("Invalid credentials.", 'danger')

        return render_template('users/login.html', form=form)


    @app.route('/logout')
    def logout():
        """Handle logout of user."""
        logout_user()
        flash("You have been logged out!", "success")
        return redirect("/login")

    @app.route('/user/<username>', methods=['GET'])
    def user_profile(username):
        """Display user's profile."""
        user = User.query.options(joinedload(User.user_boards)).filter_by(username=username).first_or_404()
        form = UserAddForm()

        # The image URL is stored in `user.image_url`
        image_url = user.image_url

        # Print debugging information
        print(f"Username: {username}")
        print(f"User: {user}")
        print(f"Image URL: {image_url}")

        return render_template('users/user_profile.html', user=user, form=form, image_url=image_url)
    
    @app.route('/list_board', methods=['GET', 'POST'])
    def list_board():
        form = BoardForm()
        print("submitted form")
        if form.validate_on_submit():
            width_fraction_decimal = fraction_to_decimal(form.width_fraction.data)
            depth_fraction_decimal = fraction_to_decimal(form.depth_fraction.data)
            board_length_total = form.board_length_feet.data * 12 + form.board_length_inches.data
            # Calculate total width and depth
            width_total = float(form.width_integer.data) + (width_fraction_decimal if width_fraction_decimal else 0)
            depth_total = float(form.depth_integer.data) + (depth_fraction_decimal if depth_fraction_decimal else 0)
            
            # Get the main photo from the form
            main_photo_file = request.files['main_photo']
            main_photo_filename = secure_filename(main_photo_file.filename)
            # Upload the main photo to Google Cloud Storage
            upload_blob(main_photo_file, main_photo_filename)
            # Get the URL of the uploaded main photo
            main_photo_url = f"https://storage.googleapis.com/board-market/{main_photo_filename}"
            
            # Create a new board with the form data
            new_board = Board(
                user_id= current_user.id,
                asking_price=form.asking_price.data,
                board_manufacturer=form.board_manufacturer.data,
                board_length_feet=form.board_length_feet.data,
                board_length_inches=form.board_length_inches.data,
                board_length_total=board_length_total,
                condition=form.condition.data,
                sell_or_rent=form.sell_or_rent.data,
                board_location=form.board_location.data,
                delivery_options=form.delivery_options.data,
                model=form.model.data,
                width_integer=form.width_integer.data,
                width_fraction=width_fraction_decimal,
                width_total=width_total,  # Add total width to the board
                depth_integer=form.depth_integer.data,
                depth_fraction=depth_fraction_decimal,
                depth_total=depth_total,  # Add total depth to the board
                volume_litres=form.volume_litres.data,
                extra_details=form.extra_details.data,
                main_photo=main_photo_url,  # Add main_photo URL to the board
                extra_photos=form.extra_photos.data  # Add extra_photos to the board
            )
            # Add the new board to the database session and commit it
            db.session.add(new_board)
            db.session.commit()
            flash('Board listed successfully!', 'success')
            print("valid form")
            return redirect(url_for('index'))
        else:
            print("not valid")
            print(form.errors)
        return render_template('list_board.html', form=form)

    from flask import session

    @app.route('/search_boards', methods=['GET'])
    def search_boards():
        # Preprocess request arguments
        args = {k: v for k, v in request.args.items() if v != 'None'}

        # Create a MultiDict with preprocessed arguments
        formdata = MultiDict(args)

        # Create form with preprocessed arguments
        form = SearchForm(formdata)

        # Convert 'None' string to None
        for field in form:
            if field.data == 'None':
                field.data = None

        print(f"Form data in search_boards: {form.data}")
        query = Board.query  # start with a base query
        
        # If there's no args in the request or the form is not valid
        if not request.args or not form.validate():
            # Populate the form with session data
            form.min_length.data = session.get('min_length')
            form.max_length.data = session.get('max_length')
            form.min_price.data = session.get('min_price')
            form.max_price.data = session.get('max_price')
            form.min_width.data = session.get('min_width')
            form.max_width.data = session.get('max_width')
            form.min_depth.data = session.get('min_depth')
            form.max_depth.data = session.get('max_depth')
            form.min_volume.data = session.get('min_volume')
            form.max_volume.data = session.get('max_volume')
            form.sell_or_rent.data = session.get('sell_or_rent')
            form.board_location.data = session.get('board_location')
            form.board_manufacturer.data = session.get('board_manufacturer')
            form.model.data = session.get('model')
            form.condition.data = session.get('condition')
            form.delivery_options.data = session.get('delivery_options')

        if request.args and form.validate():
            query = apply_filters(query, form)
            session['min_length'] = form.min_length.data
            session['max_length'] = form.max_length.data
            session['min_price'] = form.min_price.data
            session['max_price'] = form.max_price.data
            session['min_width'] = form.min_width.data
            session['max_width'] = form.max_width.data
            session['min_depth'] = form.min_depth.data
            session['max_depth'] = form.max_depth.data
            session['min_volume'] = form.min_volume.data
            session['max_volume'] = form.max_volume.data
            session['sell_or_rent'] = form.sell_or_rent.data
            session['board_location'] = form.board_location.data
            session['board_manufacturer'] = form.board_manufacturer.data
            session['model'] = form.model.data
            session['condition'] = form.condition.data
            session['delivery_options'] = form.delivery_options.data
            
        boards = query.all()  # execute the query
        # Check if the user is authenticated before querying the user's favourites
        if current_user.is_authenticated:
            favourites = Favourites.query.filter_by(user_id=current_user.id).all()
        else:
            favourites = []

        if request.args and not form.validate():
            flash('Invalid form data...', 'error')
            print("********************************************************************************")
            print(form.errors)
            print("********************************************************************************")
            print(form.min_length.data, form.max_length.data, form.min_price.data, form.max_price.data, form.min_width.data, form.max_width.data, form.min_depth.data, form.max_depth.data, form.min_volume.data, form.max_volume.data)

        return render_template('search_boards.html', form=form, boards=boards, favourites=favourites, convert_inches_to_feet=convert_inches_to_feet, convert_decimal_to_fraction=convert_decimal_to_fraction) # pass boards and favourites to the template

    @app.route('/delete_board/<int:board_id>', methods=['POST'])
    def delete_board(board_id):
        board = Board.query.get(board_id)
        if board:
            db.session.delete(board)
            db.session.commit()
            flash('Board deleted successfully.')
        else:
            flash('Board not found.')
        return redirect(url_for('search_boards'))


    @app.route('/toggle_favourite/<int:board_id>', methods=['POST'])
    @login_required
    def toggle_favourite(board_id):
        board = Board.query.get_or_404(board_id)
        if board in current_user.favourite_boards:
            current_user.favourite_boards.remove(board)
            action = 'removed'
        else:
            current_user.favourite_boards.append(board)
            action = 'added'
        db.session.commit()
        return jsonify(success=True, action=action)
    
    @app.route('/update_location', methods=['POST'])
    def update_location():
        data = request.get_json()
        current_user.location_text = data['location_text']
        current_user.coordinates = data['coordinates']
        db.session.commit()
        return jsonify({'message': 'Location updated'}), 200

    
    return app

    

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)