from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from config import Config
from models import db, User, Customer, Equipment, PurchaseOrder, WorkOrder, CalibrationSession, UncertaintyRecord, ReferenceInstrument
from forms import (
    RegistrationForm, LoginForm, CustomerForm, EquipmentForm,
    POForm, WorkOrderForm, CalibrationForm, UncertaintyForm
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Authentication routes (register, login, logout)

# CUSTOMER CRUD
@app.route('/customers')
@login_required
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/customer/new', methods=['GET','POST'])
@login_required
def new_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        c = Customer(name=form.name.data, contact_person=form.contact_person.data,
                     email=form.email.data, phone=form.phone.data)
        db.session.add(c)
        db.session.commit()
        flash('Customer added.', 'success')
        return redirect(url_for('customers'))
    return render_template('customer_form.html', form=form)

@app.route('/customer/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit_customer(id):
    c = Customer.query.get_or_404(id)
    form = CustomerForm(obj=c)
    if form.validate_on_submit():
        form.populate_obj(c)
        db.session.commit()
        flash('Customer updated.', 'success')
        return redirect(url_for('customers'))
    return render_template('customer_form.html', form=form)

@app.route('/customer/<int:id>/delete', methods=['POST'])
@login_required
def delete_customer(id):
    c = Customer.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash('Customer deleted.', 'danger')
    return redirect(url_for('customers'))

# Similar CRUD routes for Equipment, PurchaseOrder, WorkOrder, CalibrationSession, UncertaintyRecord

if __name__ == '__main__':
    app.run(debug=True)