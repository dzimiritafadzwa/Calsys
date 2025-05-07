from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, FloatField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin','Admin'),('technician','Technician')], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CustomerForm(FlaskForm):
    name = StringField('Customer Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person')
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone')
    submit = SubmitField('Save')

class EquipmentForm(FlaskForm):
    name = StringField('Equipment Name', validators=[DataRequired()])
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    description = TextAreaField('Description')
    reference_instrument_id = SelectField('Reference Instrument', coerce=int)
    submit = SubmitField('Save')

class POForm(FlaskForm):
    po_number = StringField('PO Number', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    customer_id = SelectField('Customer', coerce=int)
    equipments = SelectField('Equipments', coerce=int, choices=[], render_kw={"multiple": True})
    submit = SubmitField('Save')

class WorkOrderForm(FlaskForm):
    wo_number = StringField('WO Number', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    purchase_order_id = SelectField('Purchase Order', coerce=int)
    technician_id = SelectField('Technician', coerce=int)
    submit = SubmitField('Save')

class CalibrationForm(FlaskForm):
    instrument_id = SelectField('Equipment', coerce=int)
    work_order_id = SelectField('Work Order', coerce=int)
    start_time = DateTimeField('Start Time', validators=[DataRequired()])
    end_time = DateTimeField('End Time', validators=[DataRequired()])
    results = TextAreaField('Results')
    submit = SubmitField('Save')

class UncertaintyForm(FlaskForm):
    session_id = SelectField('Calibration Session', coerce=int)
    description = TextAreaField('Description')
    value = FloatField('Uncertainty Value', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    submit = SubmitField('Save')
