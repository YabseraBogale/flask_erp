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
    email=db.Column(db.String,nullable=False,unique=True)
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
    emergency_contact_fyida_id=db.Column(db.Integer,db.ForeignKey("EmergencyContact.fyida_id"),nullable=False) 
    firstname=db.Column(db.String,nullable=False)
    middlename=db.Column(db.String,nullable=False)
    lastname=db.Column(db.String,nullable=False)
    gender=db.Column(db.String,nullable=False)
    phonenumber=db.Column(db.String,nullable=False)
    date_of_employement=db.Column(db.DateTime(timezone=True),nullable=False)
    email=db.Column(db.String,nullable=False,unique=True)
    location=db.Column(db.String,nullable=False)
    fyida_id=db.Column(db.String,nullable=False)
    position=db.Column(db.String,nullable=False)
    department=db.Column(db.String,nullable=False)
    job_description=db.Column(db.String,nullable=False)
    tin_number=db.Column(db.Integer,nullable=False)
    bank_account_number=db.Column(db.Integer,nullable=False)
    salary=db.Column(db.Float,nullable=False)
    pension_balance=db.Column(db.Float)
    password=db.Column(db.String,nullable=False)

    emergencycontact=db.relationship("EmergencyContact")

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
            "salary":self.salary,
            "password":self.password,
            "pension_balance":self.pension_balance
        }

class Item(db.Model):

    __tablename__="Item"

    item_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_name=db.Column(db.String,nullable=False,unique=True)
    item_description=db.Column(db.String,nullable=False)
    item_price=db.Column(db.Float,nullable=False)
    item_quantity=db.Column(db.Integer,nullable=False)
    category=db.Column(db.String,nullable=False)
    subcategory=db.Column(db.String,nullable=False)
    unit=db.Column(db.String,nullable=False)
    location=db.Column(db.String,nullable=False)
    item_shelf_life=db.Column(db.DateTime(timezone=True))
    created_at=db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at=db.Column(db.DateTime(timezone=True), onupdate=func.now())
    created_by_employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"),nullable=False)
    
    employee=db.relationship("Employee")

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

class CheckOut(db.Model):

    __tablename__="CheckOut"

    checkout_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_name=db.Column(db.String,db.ForeignKey("Item.item_name"),nullable=False)
    employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"),nullable=False)
    return_employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"),nullable=False)
    item_quantity=db.Column(db.Integer,nullable=False)
    item_siv=db.Column(db.Integer,nullable=False)
    department=db.Column(db.String)
    location=db.Column(db.String)
    unit=db.Column(db.String,nullable=False)
    checkout_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    item_description=db.Column(db.String)

    employee=db.relationship("Employee")
    item=db.relationship("Item")

    def to_dict(self):
        return {
            "checkout_id":self.checkout_id,
            "item_name":self.item_name,
            "employee_id":self.employee_id,
            "return_employee_id":self.return_employee_id,
            "checkout_date":self.checkout_date,
            "item_description":self.item_description,
            "item_siv":self.item_siv,
            "department":self.department,
            "location":self.location,
            "unit":self.unit
        }

class CheckIn(db.Model):

    __tablename__="CheckIn"

    checkin_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    item_name=db.Column(db.String,db.ForeignKey("Item.item_name"),nullable=False)
    employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"),nullable=False)
    unit=db.Column(db.String,nullable=False)
    item_price=db.Column(db.Float,nullable=False)
    item_quantity=db.Column(db.Integer,nullable=False)
    item_grr=db.Column(db.Integer,nullable=False)
    reciving_employee_id=db.Column(db.Integer,db.ForeignKey("Employee.employee_id"),nullable=False)
    checkin_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    item_description=db.Column(db.String)
    
    employee=db.relationship("Employee")
    item=db.relationship("Item")
    def to_dict(self):
        return {
            "checkin_id":self.checkin_id,
            "item_name":self.item_name,
            "employee_id":self.employee_id,
            "reciving_employee_id":self.reciving_employee_id,
            "checkin_date":self.checkin_date,
            "unit":self.unit,
            "item_grr":self.item_grr,
            "item_quantity":self.item_quantity,
            "item_price":self.item_price,
            "item_description":self.item_description
        }
