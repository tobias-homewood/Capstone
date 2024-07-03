from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, TextAreaField, PasswordField, MultipleFileField, ValidationError
from wtforms.validators import InputRequired, Email, Length, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed

# Custom validator
def validate_photo_count(form, field):
    if len(field.data) > 7:
        raise ValidationError('No more than 7 photos are allowed.')
    
# Form for adding a new user
class UserAddForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    image_file = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    bio = TextAreaField('Bio', validators=[Optional()])

# Form for user login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

# Form for adding a new board
class BoardForm(FlaskForm):
    user_id = StringField('User ID')
    asking_price = DecimalField('Asking Price (€)', validators=[InputRequired()])
    board_manufacturer = StringField('Board Manufacturer', validators=[InputRequired()])
    board_length_feet = SelectField('Board Length (Feet)', choices=[(str(i), str(i)) for i in range(16)], validators=[InputRequired()])
    board_length_inches = SelectField('Board Length (Inches)', choices=[(str(i), str(i)) for i in range(12)], validators=[InputRequired()])     
    condition = SelectField('Condition', choices=[('New', 'New'), ('Used - Excellent', 'Used - Excellent'), ('Used - Great', 'Used - Great'), ('Used - Good', 'Used - Good'), ('Used - Poor', 'Used - Poor')], validators=[InputRequired()])    
    sell_or_rent = SelectField('Sell or Rent', choices=[('For sale', 'For sale'), ('For rent', 'For rent')], validators=[InputRequired()])    
    board_location_text = StringField('Board Location', validators=[InputRequired()])
    board_location_coordinates = StringField('Board Location Coordinates', validators=[InputRequired()])
    delivery_options = SelectField('Collection / Delivery', choices=[('Pick up only', 'Pick up only'), ('Local delivery', 'Local delivery'), ('National delivery', 'National delivery'), ('International delivery', 'International delivery')], validators=[InputRequired()])    
    model = StringField('Model')
    width_integer = SelectField('Width Integer', choices=[(str(i), str(i)) for i in range(15, 26)], validators=[InputRequired()])
    width_fraction = SelectField('Width Fraction', choices=[(f'{i}/16', f'{i}/16') for i in range(0, 16)], validators=[InputRequired()])    
    depth_integer = SelectField('Depth Integer', choices=[(str(i), str(i)) for i in [2, 3, 4]], validators=[InputRequired()])
    depth_fraction = SelectField('Depth Fraction', choices=[(f'{i}/16', f'{i}/16') for i in range(0, 16)], validators=[InputRequired()])    
    volume_litres = DecimalField('Volume (Litres)', places=2, rounding=None, validators=[InputRequired()])
    extra_details = TextAreaField('Extra Details', validators=[Length(max=255)])
    main_photo = FileField('Main Photo', validators=[FileAllowed(['jpg', 'png','jpeg']), InputRequired()])
    extra_photos = MultipleFileField('Extra Photos', validators=[FileAllowed(['jpg', 'png','jpeg']), Optional(), validate_photo_count])

# Form for searching boards
class SearchForm(FlaskForm):
    asking_price = DecimalField('Asking Price', places=2, rounding=None, validators=[Optional()])
    min_price = DecimalField('Minimum Price', places=2, rounding=None, validators=[Optional()])
    max_price = DecimalField('Maximum Price', places=2, rounding=None, validators=[Optional()])
    board_manufacturer = StringField('Board Manufacturer', validators=[Optional()])
    board_length_feet = SelectField('Board Length (Feet)', choices=[('', 'Any')] + [(str(i), str(i)) for i in range(16)], validators=[Optional()])
    board_length_inches = SelectField('Board Length (Inches)', choices=[('', 'Any')] + [(str(i), str(i)) for i in range(12)], validators=[Optional()]) 
    min_length = IntegerField('Minimum Length', validators=[Optional()])
    max_length = IntegerField('Maximum Length', validators=[Optional()])
    condition = SelectField('Condition', choices=[('', 'Any'), ('New', 'New'), ('Used - Excellent', 'Used - Excellent'), ('Used - Great', 'Used - Great'), ('Used - Good', 'Used - Good'), ('Used - Poor', 'Used - Poor')], validators=[Optional()])    
    sell_or_rent = SelectField('Sell or Rent', choices=[('', 'Any'), ('For sale', 'For sale'), ('For rent', 'For rent')], validators=[Optional()])    
    board_location_text = StringField('Board Location', validators=[Optional()])
    board_location_coordinates = StringField('Board Location Coordinates', validators=[Optional()])
    max_distance = IntegerField('Distance from me (km)', default=50, validators=[Optional(), NumberRange(min=1)])
    delivery_options = SelectField('Collection / Delivery', choices=[('', 'Any'), ('Pick up only', 'Pick up only'), ('Local delivery', 'Local delivery'), ('National delivery', 'National delivery'), ('International delivery', 'International delivery')], validators=[Optional()])    
    model = StringField('Model', validators=[Optional()])
    width_integer = SelectField('Width Integer', choices=[('', 'Any')] + [(str(i), str(i)) for i in range(15, 26)], validators=[Optional()])
    width_fraction = SelectField('Width Fraction', choices=[('', 'Any')] + [(f'{i}/16', f'{i}/16') for i in range(0, 16)], validators=[Optional()])    
    min_width = DecimalField('Minimum Width', places=5, rounding=None, validators=[Optional()])
    max_width = DecimalField('Maximum Width', places=5, rounding=None, validators=[Optional()])
    depth_integer = SelectField('Depth Integer', choices=[('', 'Any')] + [(str(i), str(i)) for i in [2, 3, 4]], validators=[Optional()])
    depth_fraction = SelectField('Depth Fraction', choices=[('', 'Any')] + [(f'{i}/16', f'{i}/16') for i in range(0, 16)], validators=[Optional()])    
    min_depth = DecimalField('Minimum Depth', places=5, rounding=None, validators=[Optional()])
    max_depth = DecimalField('Maximum Depth', places=5, rounding=None, validators=[Optional()])
    volume_litres = DecimalField('Volume (Litres)', places=2, rounding=None, validators=[Optional()])
    min_volume = DecimalField('Minimum Volume (Litres)', places=2, rounding=None, validators=[Optional()])
    max_volume = DecimalField('Maximum Volume (Litres)', places=2, rounding=None, validators=[Optional()])
    