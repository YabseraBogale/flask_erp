from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db=SQLAlchemy()


class EmergencyContact(db.Model):
    __tablename__="EmergencyContact"

    fyida_id=db.Column(db.String,primary_key=True) 
    firstname=db.Column(db.String,nullable=False)
    middlename=db.Column(db.String,nullable=False)
    lastname=db.Column(db.String,nullable=False)
    gender=db.Column(db.String,nullable=False)
    phonenumber=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    location=db.Column(db.String,nullable=False)
    


class Employee(db.Model):

    __tablename__="Employee"
    employee_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    emergency_contact_fyida_id=db.Column(db.Integer,db.ForeignKey("EmergencyContact.fyida_id")) 
    firstname=db.Column(db.String,nullable=False)
    middlename=db.Column(db.String,nullable=False)
    lastname=db.Column(db.String,nullable=False)
    gender=db.Column(db.String,nullable=False)
    phonenumber=db.Column(db.String,nullable=False)
    date_of_employement=db.Column(db.DateTime(timezone=True),nullable=False)
    email=db.Column(db.String,nullable=False)
    location=db.Column(db.String,nullable=False)
    fyida_id=db.Column(db.String,nullable=False)
    position=db.Column(db.String,nullable=False)
    department=db.Column(db.String,nullable=False)
    job_description=db.Column(db.String,nullable=False)
    tin_number=db.Column(db.Integer,nullable=False)
    bank_account_number=db.Column(db.Integer,nullable=False)
    salary=db.Column(db.Float,nullable=False)

class Item(db.Model):

    __tablename__="Item"

    item_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_name=db.Column(db.String,nullable=False)
    item_description=db.Column(db.String,nullable=False)
    item_price=db.Column(db.Float,nullable=False)
    item_quantity=db.Column(db.Integer,nullable=False)
    category=db.Column(db.String,nullable=False)
    subcategory=db.Column(db.String,nullable=False)
    unit=db.Column(db.String,nullable=False)
    location=db.Column(db.String,nullable=False)
    created_at=db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at=db.Column(db.DateTime(timezone=True), onupdate=func.now())
    created_by_employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"))
    

class TransactionType(db.Model):

    __tablename__="TransactionType"

    transaction_type_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    type_name=db.Column(db.String,nullable=False,unique=True)


class ItemLog(db.Model):

    __tablename__="ItemLog"

    log_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_id=db.Column(db.Integer,db.ForeignKey("Item.item_id"))
    transaction_type_name=db.Column(db.String,db.ForeignKey("TransactionType.type_name"))
    employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"))
    quantity_changed=db.Column(db.Integer,nullable=False)
    transaction_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    description=db.Column(db.String,nullable=False)

class Checkout(db.Model):

    __tablename__="Checkout"

    checkout_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_id=db.Column(db.Integer,db.ForeignKey("Item.item_id"))
    employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"))
    revice_employee=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"))
    checkout_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    notes=db.Column(db.String)


class CheckIn(db.Model):

    __tablename__="Checkout"

    checkin_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_id=db.Column(db.Integer,db.ForeignKey("Item.item_id"))
    employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"))
    returning_employee=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"))
    checkin_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    notes=db.Column(db.String)
