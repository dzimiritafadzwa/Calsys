from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='technician')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    contact_person = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    purchase_orders = db.relationship('PurchaseOrder', backref='customer', lazy='dynamic')

class ReferenceInstrument(db.Model):
    __tablename__ = 'reference_instruments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    serial_number = db.Column(db.String(120), unique=True, nullable=False)
    calibration_date = db.Column(db.Date)
    uncertainty = db.Column(db.Text)
    equipments = db.relationship('Equipment', backref='reference_instrument', lazy='dynamic')

po_equipment = db.Table('po_equipment',
    db.Column('po_id', db.Integer, db.ForeignKey('purchase_order.id')),
    db.Column('equipment_id', db.Integer, db.ForeignKey('equipment.id'))
)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    serial_number = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    reference_instrument_id = db.Column(db.Integer, db.ForeignKey('reference_instruments.id'))

class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(64), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    equipments = db.relationship('Equipment', secondary=po_equipment, backref='purchase_orders')
    work_orders = db.relationship('WorkOrder', backref='purchase_order', lazy='dynamic')

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wo_number = db.Column(db.String(64), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'))
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    calibration_sessions = db.relationship('CalibrationSession', backref='work_order', lazy='dynamic')

class CalibrationSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instrument_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    results = db.Column(db.Text)
    uncertainties = db.relationship('UncertaintyRecord', backref='session', lazy='dynamic')

class UncertaintyRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('calibration_session.id'))
    description = db.Column(db.Text)
    value = db.Column(db.Float)
    unit = db.Column(db.String(20))