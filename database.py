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
    
    def to_dict(self):
        return {
            "fyida_id":self.fyida_id,
            "firstname":self.firstname,
            "middlename":self.middlename,
            "lastname":self.lastname,
            "gender":self.gender,
            "phonenumber":self.phonenumber,
            "email":self.email,
            "location":self.location
        }


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

    def to_dict(self):
        return {
            "fyida_id":self.fyida_id,
            "firstname":self.firstname,
            "middlename":self.middlename,
            "lastname":self.lastname,
            "gender":self.gender,
            "phonenumber":self.phonenumber,
            "email":self.email,
            "location":self.location,
            "date_of_employement":self.date_of_employement,
            "emergency_contact_fyida_id":self.emergency_contact_fyida_id,
            "position":self.position,
            "department":self.department,
            "job_description":self.job_description,
            "tin_number":self.tin_number,
            "bank_account_number":self.bank_account_number,
            "salary":self.salary
        }

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
    
    def to_dict(self):
        return {
            "item_id":self.item_id,
            "item_name":self.item_name,
            "item_description":self.item_description,
            "category":self.category,
            "subcategory":self.subcategory,
            "item_price":self.item_price,
            "item_quantity":self.item_quantity,
            "location":self.location,
            "created_by_employee_id":self.created_by_employee_id,
            "created_at":self.created_at,
            "updated_at":self.updated_at,
            "unit":self.unit
        }

class TransactionType(db.Model):

    __tablename__="TransactionType"

    transaction_type_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    type_name=db.Column(db.String,nullable=False,unique=True)

    def to_dict(self):
        return {
            "transaction_type_id":self.transaction_type_id,
            "type_name":self.type_name
        }

class ItemLog(db.Model):

    __tablename__="ItemLog"

    log_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_name=db.Column(db.Integer,db.ForeignKey("Item.item_name"))
    transaction_type_name=db.Column(db.String,db.ForeignKey("TransactionType.type_name"))
    employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"))
    quantity_changed=db.Column(db.Integer,nullable=False)
    item_price=db.Column(db.Float,nullable=False)
    transaction_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    description=db.Column(db.String,nullable=False)

    def to_dict(self):
        return {
            "log_id":self.log_id,
            "item_name":self.item_name,
            "":self.transaction_type_name,
            "employee_id":self.employee_id,
            "quantity_changed":self.quantity_changed,
            "description":self.description,
            "item_price":self.item_price,
        }

class Checkout(db.Model):

    __tablename__="Checkout"

    checkout_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_id=db.Column(db.Integer,db.ForeignKey("Item.item_id"))
    employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"))
    revice_employee_name=db.Column(db.String)
    checkout_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    notes=db.Column(db.String)

    def to_dict(self):
        return {
            "checkout_id":self.checkout_id,
            "item_id":self.item_id,
            "employee_id":self.employee_id,
            "revice_employee_name":self.revice_employee_name,
            "checkout_date":self.checkout_date,
            "notes":self.notes
        }

class CheckIn(db.Model):

    __tablename__="CheckIn"

    checkin_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_id=db.Column(db.Integer,db.ForeignKey("Item.item_id"))
    employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"))
    returning_employee_name=db.Column(db.String)
    checkin_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    notes=db.Column(db.String)

    def to_dict(self):
        return {
            "checkin_id":self.checkin_id,
            "item_id":self.item_id,
            "employee_id":self.employee_id,
            "returning_employee_name":self.returning_employee_name,
            "checkin_date":self.checkin_date,
            "notes":self.notes
        }
