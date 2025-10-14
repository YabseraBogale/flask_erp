import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin


db=SQLAlchemy()

class Location(db.Model):

    __tablename__="Location"

    location=db.Column(db.String,primary_key=True)

    def to_dict(self):
        return {
            "location":self.location
        }

class Unit(db.Model):
    __tablename__="Unit"

    unit=db.Column(db.String,primary_key=True)

    def to_dict(self):
        return {
            "unit":self.unit
        }

class Category(db.Model):

    __tablename__="Category"

    category=db.Column(db.String,primary_key=True)

    def to_dict(self):
        return {
            "category":self.category
        }

class Department(db.Model):

    __tablename__="Department"

    department=db.Column(db.String,primary_key=True)

    def to_dict(self):
        return {
            "department":self.department
        }


class Currency(db.Model):

    __tablename__="Currency"

    currency=db.Column(db.String,primary_key=True)
    def to_dict(self):
        return {
            "currency":self.currency
        }
    
class Subcategory(db.Model):

    __tablename__="Subcategory"

    subcategory=db.Column(db.String,primary_key=True)

    def to_dict(self):
        return {
            "subcategory":self.subcategory
        }

class EmergencyContact(db.Model):

    __tablename__="EmergencyContact"

    fyida_id=db.Column(db.String,primary_key=True) 
    firstname=db.Column(db.String,nullable=False)
    middlename=db.Column(db.String,nullable=False)
    lastname=db.Column(db.String,nullable=False)
    gender=db.Column(db.String,nullable=False)
    phonenumber=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False,unique=True)
    location_name=db.Column(db.String,db.ForeignKey("Location.location"),nullable=False)
    
    location=db.relationship("Location",foreign_keys=[location_name])

    def to_dict(self):
        return {
            "fyida_id":self.fyida_id,
            "firstname":self.firstname,
            "middlename":self.middlename,
            "lastname":self.lastname,
            "gender":self.gender,
            "phonenumber":self.phonenumber,
            "email":self.email,
            "location_name":self.location_name
        }


class Employee(db.Model,UserMixin):

    __tablename__="Employee"

    employee_tin_number=db.Column(db.Integer,nullable=False)
    firstname=db.Column(db.String,nullable=False)
    middlename=db.Column(db.String,nullable=False)
    lastname=db.Column(db.String,nullable=False)
    gender=db.Column(db.String,nullable=False)
    phonenumber=db.Column(db.String,nullable=False)
    date_of_employement=db.Column(db.DateTime(timezone=True),nullable=False)
    email=db.Column(db.String,nullable=False,unique=True)
    fyida_id=db.Column(db.String,nullable=False)
    position=db.Column(db.String,nullable=False)
    job_description=db.Column(db.String,nullable=False)
    bank_account_number=db.Column(db.Integer,nullable=False)
    salary=db.Column(db.Float,nullable=False)
    pension_balance=db.Column(db.Float)
    password=db.Column(db.String,nullable=False)
    employment_status = db.Column(Enum(
                "Active", "Resigned", "Terminated",
                "Deceased", "Retired", name="employment_status_enum"),
                default="Active",nullable=False)
    termination_reason = db.Column(db.String)
    termination_date = db.Column(db.DateTime(timezone=True))
    emergency_contact_fyida_id=db.Column(db.String,db.ForeignKey("EmergencyContact.fyida_id"),nullable=False) 
    department_name=db.Column(db.String,db.ForeignKey("Department.department"),nullable=False)
    location_name=db.Column(db.String,db.ForeignKey("Location.location"),nullable=False)
    currency_name=db.Column(db.String,db.ForeignKey("Currency.currency"),nullable=False)

    emergencycontact=db.relationship("EmergencyContact",foreign_keys=[emergency_contact_fyida_id])
    location=db.relationship("Location",foreign_keys=[location_name])
    currency=db.relationship("Currency",foreign_keys=[currency_name])
    department=db.relationship("Department",foreign_keys=[department_name])

    def to_dict(self):
        return {
                          "employee_tin_number":self.employee_tin_number,
            "fyida_id":self.fyida_id,
            "firstname":self.firstname,
            "middlename":self.middlename,
            "lastname":self.lastname,
            "gender":self.gender,
            "phonenumber":self.phonenumber,
            "email":self.email,
            "location_name":self.location_name,
            "date_of_employement":self.date_of_employement,
            "emergency_contact_fyida_id":self.emergency_contact_fyida_id,
            "position":self.position,
            "department_name":self.department_name,
            "job_description":self.job_description,
            "bank_account_number":self.bank_account_number,
            "salary":self.salary,
            "password":self.password,
            "employment_status":self.employment_status,
            "termination_date":self.termination_date,
            "termination_reason":self.termination_reason,
            "pension_balance":self.pension_balance,
            "currency_name":self.currency_name
        }

    def get_id(self):
        return str(self.employee_tin_number)
    
    
class Item(db.Model):

    __tablename__="Item"

    item_id=db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    item_name=db.Column(db.String,nullable=False,unique=True)
    item_description=db.Column(db.String,nullable=False)
    item_price=db.Column(db.Float,nullable=False)
    item_quantity=db.Column(db.Float,nullable=False)
    item_shelf_life=db.Column(db.DateTime(timezone=True))
    created_at=db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at=db.Column(db.DateTime(timezone=True), onupdate=func.now())

    unit_name=db.Column(db.String,db.ForeignKey("Unit.unit"),nullable=False)
    created_by_employee_tin_number=db.Column(db.Integer,db.ForeignKey("Employee.employee_tin_number"),nullable=False)
    location_name=db.Column(db.String,db.ForeignKey("Location.location"),nullable=False)
    category_name=db.Column(db.String,db.ForeignKey("Category.category"),nullable=False)
    currency_name=db.Column(db.String,db.ForeignKey("Currency.currency"),nullable=False)
    subcategory_name=db.Column(db.String,db.ForeignKey("Subcategory.subcategory"),nullable=False)
    
    unit=db.relationship("Unit",foreign_keys=[unit_name])
    location=db.relationship("Location",foreign_keys=[location_name])
    currency=db.relationship("Currency",foreign_keys=[currency_name])
    employee=db.relationship("Employee",foreign_keys=[created_by_employee_tin_number])
    category=db.relationship("Category",foreign_keys=[category_name])
    subcategory=db.relationship("Subcategory",foreign_keys=[subcategory_name])

    def to_dict(self):
        return {
            "item_id":self.item_id,
            "item_name":self.item_name,
            "item_description":self.item_description,
            "category_name":self.category_name,
            "subcategory_name":self.subcategory_name,
            "item_price":self.item_price,
            "item_quantity":self.item_quantity,
            "location_name":self.location_name,
            "created_by_employee_tin_number":self.created_by_employee_tin_number,
            "created_at":self.created_at,
            "updated_at":self.updated_at,
            "unit_name":self.unit_name,
            "currency_name":self.currency_name
        }

class CheckOut(db.Model):

    __tablename__="CheckOut"

    checkout_id=db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    
    item_quantity=db.Column(db.Float,nullable=False)
    item_siv=db.Column(db.Integer,nullable=False)
    checkout_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    item_description=db.Column(db.String)
    item_name=db.Column(db.String,db.ForeignKey("Item.item_name"),nullable=False)
    employee_tin_number=db.Column(UUID(as_uuid=True),db.ForeignKey("Employee.employee_tin_number"),nullable=False)
    return_employee_tin_number=db.Column(db.Integer,db.ForeignKey("Employee.employee_tin_number"),nullable=False)
    location_name=db.Column(db.String,db.ForeignKey("Location.location"),nullable=False)
    department_name=db.Column(db.String,db.ForeignKey("Department.department"),nullable=False)
    unit_name=db.Column(db.String,db.ForeignKey("Unit.unit"),nullable=False)
    

    department=db.relationship("Department",foreign_keys=[department_name])
    location=db.relationship("Location",foreign_keys=[location_name])
    employee=db.relationship("Employee",foreign_keys=[employee_tin_number])
    return_employee=db.relationship("Employee",foreign_keys=[return_employee_tin_number])
    item=db.relationship("Item",foreign_keys=[item_name])
    unit=db.relationship("Unit",foreign_keys=[unit_name])
    
    def to_dict(self):
        return {
            "checkout_id":self.checkout_id,
            "item_name":self.item_name,
            "employee_tin_number":self.employee_tin_number,
            "return_employee_tin_number":self.return_employee_tin_number,
            "checkout_date":self.checkout_date,
            "item_description":self.item_description,
            "item_siv":self.item_siv,
            "department_name":self.department_name,
            "location_name":self.location_name,
            "unit_name":self.unit_name
        }

class CheckIn(db.Model):

    __tablename__="CheckIn"

    checkin_id=db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    item_name=db.Column(db.String,db.ForeignKey("Item.item_name"),nullable=False)
    item_price=db.Column(db.Float,nullable=False)
    item_quantity=db.Column(db.Float,nullable=False)
    item_grr=db.Column(db.Integer,nullable=False)
    checkin_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    item_description=db.Column(db.String)
    employee_tin_number=db.Column(db.Integer,db.ForeignKey("Employee.employee_tin_number"),nullable=False)
    reciving_employee_tin_number=db.Column(db.Integer,db.ForeignKey("Employee.employee_tin_number"),nullable=False)
    currency_name=db.Column(db.String,db.ForeignKey("Currency.currency"),nullable=False)
    unit_name=db.Column(db.String,db.ForeignKey("Unit.unit"),nullable=False)
    
    currency=db.relationship("Currency",foreign_keys=[currency_name])
    employee=db.relationship("Employee",foreign_keys=[employee_tin_number])
    reciving_employee=db.relationship("Employee",foreign_keys=[reciving_employee_tin_number])
    item=db.relationship("Item",foreign_keys=[item_name])
    unit=db.relationship("Unit",foreign_keys=[unit_name])

    def to_dict(self):
        return {
            "checkin_id":self.checkin_id,
            "item_name":self.item_name,
            "employee_tin_number":self.employee_tin_number,
            "reciving_employee_tin_number":self.reciving_employee_tin_number,
            "checkin_date":self.checkin_date,
            "unit_name":self.unit_name,
            "currency_name":self.currency_name,
            "item_grr":self.item_grr,
            "item_quantity":self.item_quantity,
            "item_price":self.item_price,
            "item_description":self.item_description
        }


class Customer(db.Model):

    __tablename__="Customer"

    customer_tin=db.Column(db.Integer,primary_key=True,nullable=False)
    customer_name=db.Column(db.String,nullable=False,unque=True)
    customer_email=db.Column(db.String,nullable=False,unique=True)
    customer_phonenumber=db.Column(db.String,nullable=False)
    customer_location=db.Column(db.String,db.ForeignKey("Location.location"),nullable=False)
    regsistered_employee_tin_number=db.Column(db.Integer,db.ForeignKey("Employee.employee_tin_number"),nullable=False)
    customer_registered_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    location=db.relationship("Location",foreign_keys=[customer_location])
    employee=db.relationship("Employee",foreign_keys=[regsistered_employee_tin_number])

    def to_dict(self):
        return {
            
            "customer_name":self.customer_name,
            "customer_email":self.customer_email,
            "customer_phonenumber":self.customer_phonenumber,
            "customer_location":self.customer_location,
            "customer_tin":self.customer_tin,
            "employee_regsistered_id":self.regsistered_employee_tin_number
        }

class Sales(db.Model):

    __tablename__="Sales"

    sales_id=db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    sales_date=db.Column(db.DateTime(timezone=True), server_default=func.now())
    item_name=db.Column(db.String,db.ForeignKey("Item.item_name"),nullable=False)
    item_quantity=db.Column(db.Integer,nullable=False)
    total_price=db.Column(db.Float,nullable=False)
    employee_tin_number=db.Column(db.Integer,db.ForeignKey("Employee.employee_tin_number"),nullable=False)
    customer_tin=db.Column(db.Integer,db.ForeignKey("Customer.customer_tin"),nullable=False)
    currency_name=db.Column(db.String,db.ForeignKey("Currency.currency"),nullable=False)
    unit_name=db.Column(db.String,db.ForeignKey("Unit.unit"),nullable=False)

    currency=db.relationship("Currency",foreign_keys=[currency_name])
    employee=db.relationship("Employee",foreign_keys=[employee_tin_number])
    item=db.relationship("Item",foreign_keys=[item_name])
    unit=db.relationship("Unit",foreign_keys=[unit_name])
    customer=db.relationship("Customer",foreign_keys=[customer_tin])

    def to_dict(self):
        return {
            "sales_id":self.sales_id,
            "item_name":self.item_name,
            "employee_id":self.employee_tin_number,
            "sales_date":self.sales_date,
            "item_quantity":self.item_quantity,
            "total_price":self.total_price,
            "currency_name":self.currency_name,
            "unit_name":self.unit_name
        }

class PurchaseOrder(db.Model):

    __tablename__="PurchaseOrder"
    
    purchase_order_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    order_date=db.Column(db.DateTime(timezone=True),server_default=func.now())
    order_status=db.Column(Enum(
                "Pending","Approved","Decline", name="order_status_enum"),
                default="Active",nullable=False)
    ordered_quantity=db.Column(db.Float,nullable=False)
    purchase_reason=db.Column(db.String,nullable=False)
    item_name=db.Column(db.String,db.ForeignKey("Item.item_name"),nullable=False)
    employee_tin_number=db.Column(db.Integer,db.ForeignKey("Employee.employee_tin_number"),nullable=False)
    
    item=db.relationship("Item",foreign_keys=[item_name])
    employee=db.relationship("Employee",foreign_keys=[employee_tin_number])
    
    def to_dict(self):
        return {
            "purchase_order_id":self.purchase_order_id,
            "employee_tin_number":self.employee_tin_number,
            "item_name":self.item_name,
            "ordered_quantity":self.ordered_quantity,
            "ordered_quantity":self.purchase_reason,
            "order_status":self.order_status,
            "order_date":self.order_date
        }