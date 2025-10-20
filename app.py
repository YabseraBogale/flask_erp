import smtplib
import os
import string
import random
import bcrypt
import logging
from sqlalchemy import update
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask import Flask,url_for,render_template,redirect,request,session,jsonify
from datetime import datetime
from sqlalchemy import event
from database import db,EmergencyContact,Employee,Item,CheckOut,CheckIn,Location,Category,Subcategory,Unit,Currency,Department,Sales,Customer,PurchaseOrder,Vendor
from email.message import EmailMessage
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logging.basicConfig(
    filename='application.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app=Flask(__name__)

company_email=os.getenv("company_email")
company_email_password=os.getenv("company_email_password")

salt = bcrypt.gensalt()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

# CRITICAL: Use SQLALCHEMY_ENGINE_OPTIONS to define a connection listener
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    # Recommended for SQLite with Flask's multi-threaded server
    "connect_args": {"check_same_thread": False}    
}

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://sqlite:///database.db",
)

db.init_app(app)
login_manager=LoginManager(app)
login_manager.login_view = "login"

with app.app_context():

    @event.listens_for(db.engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
            # Execute the necessary SQL command to enable foreign key enforcement
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        
    db.create_all()

    db_location=db.session.query(Location.location).order_by(Location.location.asc()).all()
    db_unit=db.session.query(Unit.unit).order_by(Unit.unit.asc()).all()
    db_currency=db.session.query(Currency.currency).order_by(Currency.currency.asc()).all()
    db_department=db.session.query(Department.department).order_by(Department.department.asc()).all()
    db_category=db.session.query(Category.category).order_by(Category.category.asc()).all()
    db_subcategory=db.session.query(Subcategory.subcategory).order_by(Subcategory.subcategory.asc()).all()
    item_name_list=db.session.query(Item.item_name).all()

@login_manager.user_loader
def load_user(employee_tin_number):
    return db.session.get(Employee, employee_tin_number)

@app.before_request
def logout_if_not_active():
    if current_user.is_authenticated:
        employee=db.session.get(Employee, current_user.employee_tin_number)
        if not employee or employee.employment_status!="Active":
            logout_user()
            session.clear()
            return redirect(url_for('login'))

@app.route("/employee_registeration",methods=["GET","POST"])
@login_required
def employee_registeration():
    try:
        if session["department_name"]=="Human Resources" or session["department_name"]=="Administration":
            if request.method=="POST":
                emergency_contact_fyida_id=request.form["emergency_contact_fyida_id"]
                emergency_contact_firstname=request.form["emergency_contact_firstname"]
                emergency_contact_lastname=request.form["emergency_contact_lastname"]
                emergency_contact_middlename=request.form["emergency_contact_middlename"]
                emergency_contact_gender=request.form["emergency_contact_gender"]
                emergency_contact_phonenumber="+251 "+request.form["emergency_contact_phonenumber"]
                emergency_contact_email=request.form["emergency_contact_email"]
                emergency_contact_location=request.form["emergency_contact_location"]
                
                emergency_contact=EmergencyContact(
                    firstname=emergency_contact_firstname,
                    lastname=emergency_contact_lastname,middlename=emergency_contact_middlename,
                    phonenumber=emergency_contact_phonenumber,location_name=emergency_contact_location,
                    fyida_id=emergency_contact_fyida_id,gender=emergency_contact_gender,
                    email=emergency_contact_email)
                db.session.add(emergency_contact)
                db.session.commit()

                firstname=request.form["firstname"]
                lastname=request.form["lastname"]
                middlename=request.form["middlename"]
                gender=request.form["gender"]
                phonenumber="+251 "+request.form["phonenumber"]
                email=request.form["email"]
                date_of_employement=request.form["date_of_employement"]
                date_of_employement = datetime.strptime(date_of_employement, "%Y-%m-%d").date()
                fyida_id=request.form["fyida_id"]
                position=request.form["position"]
                location=request.form["location"]
                department=request.form["department"]
                job_description=request.form["job_description"]
                tin_number=request.form["tin_number"]
                bank_account_number=request.form["bank_account_number"]
                currency=request.form["currency"]
                salary=request.form["salary"]
                characters = string.ascii_letters + string.digits + string.punctuation
                password_to_send = ''.join(random.choice(characters) for i in range(15))
                
                password=(password_to_send).encode("utf-8")
                employee=Employee(
                    emergency_contact_fyida_id=emergency_contact_fyida_id,
                    firstname=firstname,lastname=lastname,middlename=middlename,phonenumber=phonenumber,
                    gender=gender,email=email,date_of_employement=date_of_employement,fyida_id=fyida_id,
                    employee_tin_number=tin_number,currency_name=currency,
                    position=position,location_name=location,
                    department_name=department,job_description=job_description,
                    bank_account_number=bank_account_number,salary=salary,
                    password=bcrypt.hashpw(password,salt))
                
                db.session.add(employee)
                db.session.commit()

                employee=db.session.query(Employee).filter(Employee.email==email).first()
                subject="Well Come to Comapny Name"
                body=f"This sent by bot for Comapny Name password. Employee id:{employee.employee_tin_number}  Your password: {password_to_send}"
                msg = EmailMessage()
                msg['subject']=subject
                msg['From']=company_email
                msg['To'] = email
                msg.set_content(body)
                try:

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: # For Gmail, use SMTP_SSL and port 465    
                        smtp.login(company_email, company_email_password)
                        smtp.send_message(msg)
                        return render_template("employee_registeration.html")

                except Exception as e:    
                    db.session.rollback()
                    return render_template("404.html")
                return redirect("/dashboard")
            return render_template("employee_registeration.html",db_location=db_location,db_unit=db_unit,db_currency=db_currency,db_department=db_department)
        return render_template("404.html")
    
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")
    
@app.route("/employee_termination",methods=["GET","POST"])
@login_required
def employee_termination():
    try:
        if session["department_name"]=="Human Resources" or session["department_name"]=="Administration":
            if request.method=="POST":
                termination_date=request.form["termination_date"]
                termination_date=datetime.strptime(termination_date, "%Y-%m-%d").date()
                termination_reason=request.form["termination_reason"]
                employment_status=request.form["employment_status"]
                employee_tin_number=request.form["employee_tin_number"]
                stmt=(
                    update(Employee)
                    .where(Employee.employee_tin_number==employee_tin_number)
                    .values(termination_date=termination_date,
                            termination_reason=termination_reason,
                            employment_status=employment_status)
                )
                db.session.execute(stmt)
                db.session.commit()        
            return render_template("employee_termination.html",sucess=True)
        else:
            return render_template("404.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

    
@app.route("/terminated_employee_list")
@login_required
def terminated_employee_list():
    try:
        if session["department_name"]=="Human Resources" or session["department_name"]=="Administration":
            return render_template("terminated_employee_list.html",db_department=db_department,db_location=db_location)
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/terminated_employee_list/employee/data")
@login_required
def terminated_employee_list_data():
    try:
        if session["department_name"]=="Human Resources" or session["department_name"]=="Administration":
            result=db.session.query(Employee.firstname,Employee.lastname,
                                    Employee.phonenumber,Employee.department_name,
                                    Employee.position,Employee.salary,
                                    Employee.termination_date,Employee.employee_tin_number
                                    ).where(
                                        Employee.employment_status!="Active"
                                    ).all()
            lst=[]
            for i in result:
                lst.append({
                    "firstname":i[0],
                    "lastname":i[1],
                    "phonenumber":i[2],
                    "department_name":i[3],
                    "position":i[4],
                    "salary":i[5],
                    "termination_date":i[6],
                    "employee_tin_number":i[7]
                })
            return jsonify(lst)
        return render_template("404.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")


@app.route("/terminated_employee_list/employee/data/<employee_tin_number>")
@login_required
def terminated_employee_data(employee_tin_number):
    try:
        if session["department_name"]=="Human Resources" or session["department_name"]=="Administration":
            employee=db.session.query(Employee).where(Employee.employee_tin_number==employee_tin_number).first()
            emergency_contact=db.session.query(EmergencyContact).where(EmergencyContact.fyida_id==employee.emergency_contact_fyida_id).first()
            employee={
                "emergency_contact":{
                    "name":emergency_contact.firstname + " " +emergency_contact.lastname,
                    "fyida_id":emergency_contact.fyida_id,
                    "email":emergency_contact.email,
                    "gender":emergency_contact.gender,
                    "phonenumber":emergency_contact.phonenumber,
                    "location":str(emergency_contact.location).replace("<Location ","").replace(">","")
                },
                "employee_tin_number":employee.employee_tin_number,
                "location":str(employee.location).replace("<Location ","").replace(">",""),
                "department_name":employee.department_name,
                "salary":employee.salary,
                "name":employee.firstname + " " +employee.lastname,
                "fyida_id":employee.fyida_id,
                "date_of_employement":employee.date_of_employement,
                "bank_account_number":employee.bank_account_number,
                "gender":employee.gender,
                "email":employee.email,
                "job_description":employee.job_description,
                "position":employee.position,
                "termination_date":employee.termination_date,
                "termination_reason":employee.termination_reason,
                "employment_status":employee.employment_status,
            }
            return render_template("my_account.html",employee=employee,termaination=True)
        return render_template("404.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/restate/<employee_tin_number>",methods=["GET","POST"])
@login_required
def restate(employee_tin_number):
    try:
        if session["department_name"]=="Human Resources" or session["department_name"]=="Administration":
            if request.method=="POST":
                employment_status=request.form["employment_status"]
                stmt=(
                    update(
                        Employee
                    ).where(
                        Employee.employee_tin_number==employee_tin_number
                    ).values(
                        employment_status=employment_status
                    )
                )
                db.session.execute(stmt)
                db.session.commit()
                return redirect("/dashboard")
        return render_template("404.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/all/employee/data")
@login_required
def employee_data():
    try:
        if session["department_name"]=="Human Resources" or session["department_name"]=="Administration":
            result=db.session.query(Employee.firstname,Employee.lastname,
                                    Employee.phonenumber,Employee.department_name,
                                    Employee.position,Employee.salary,
                                    Employee.bank_account_number,Employee.employee_tin_number
                                    ).where(
                                        Employee.employment_status=="Active"
                                    ).all()
            lst=[]
            for i in result:
                lst.append({
                    "firstname":i[0],
                    "lastname":i[1],
                    "phonenumber":i[2],
                    "department_name":i[3],
                    "position":i[4],
                    "salary":i[5],
                    "bank_account_number":i[6],
                    "employee_tin_number":i[7]
                })
            return jsonify(lst)
        return render_template("404.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")




@app.route("/employee_info_for_hr/<employee_tin_number>")
@login_required
def employee_info_for_hr(employee_tin_number):
    try:
        if session["department_name"]=="Human Resources" or session["department_name"]=="Administration":
            employee=db.session.query(Employee).where(Employee.employee_tin_number==employee_tin_number).first()
            emergency_contact=db.session.query(EmergencyContact).where(EmergencyContact.fyida_id==employee.emergency_contact_fyida_id).first()
            employee={
                "emergency_contact":{
                    "name":emergency_contact.firstname + " " +emergency_contact.lastname,
                    "fyida_id":emergency_contact.fyida_id,
                    "email":emergency_contact.email,
                    "gender":emergency_contact.gender,
                    "phonenumber":emergency_contact.phonenumber,
                    "location":str(emergency_contact.location).replace("<Location ","").replace(">","")
                },
                "employee_tin_number":employee.employee_tin_number,
                "location":str(employee.location).replace("<Location ","").replace(">",""),
                "department_name":employee.department_name,
                "salary":employee.salary,
                "name":employee.firstname + " " +employee.lastname,
                "fyida_id":employee.fyida_id,
                "date_of_employement":employee.date_of_employement,
                "bank_account_number":employee.bank_account_number,
                "gender":employee.gender,
                "email":employee.email,
                "job_description":employee.job_description,
                "position":employee.position
            }
            return render_template("my_account.html",employee=employee)
        return render_template("404.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")




@app.route("/my_account")
@login_required
def account():
    try:
        employee=db.session.query(Employee).where(Employee.employee_tin_number==session["employee_tin_number"]).first()
        emergency_contact=db.session.query(EmergencyContact).where(EmergencyContact.fyida_id==employee.emergency_contact_fyida_id).first()
        employee={
            "emergency_contact":{
                "name":emergency_contact.firstname + " " +emergency_contact.lastname,
                "fyida_id":emergency_contact.fyida_id,
                "email":emergency_contact.email,
                "gender":emergency_contact.gender,
                "phonenumber":emergency_contact.phonenumber,
                "location":str(emergency_contact.location).replace("<Location ","").replace(">","")
            },
            "employee_tin_number":employee.employee_tin_number,
            "location":str(employee.location).replace("<Location ","").replace(">",""),
            "department_name":employee.department_name,
            "salary":employee.salary,
            "name":employee.firstname + " " +employee.lastname,
            "fyida_id":employee.fyida_id,
            "date_of_employement":employee.date_of_employement,
            "bank_account_number":employee.bank_account_number,
            "gender":employee.gender,
            "email":employee.email,
            "job_description":employee.job_description,
            "position":employee.position
        }

        return render_template("my_account.html",employee=employee)
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/all/employee")
@login_required
def all_employee():
    try:
        if session["department_name"]=="Human Resources" or session["department_name"]=="Administration":
            return render_template("all_employee.html",db_department=db_department)
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")
   
@app.route("/item_regsisteration",methods=["GET","POST"])
@login_required
def item_registeration():
    try:
        if session["department_name"]=="Store" or session["department_name"]=="Administration":
            if request.method=="POST":
                item_name=request.form["item_name"]
                item_price=request.form["item_price"]
                unit=request.form["unit"]
                location_name=request.form["location"]
                item_category=request.form["item_category"]
                item_subcategory=request.form["item_subcategory"]
                item_quantity=request.form["item_quantity"]
                item_description=request.form["item_description"]
                item_name=request.form["item_name"]
                item_shelf_life=request.form["item_shelf_life"]
                currency=request.form["currency"]
                item_shelf_life = datetime.strptime(item_shelf_life, "%Y-%m-%d").date()
                item=Item(
                    item_name=item_name,item_price=item_price,
                    currency_name=currency,item_quantity=item_quantity,
                    unit_name=unit,category_name=item_category,
                    location_name=location_name,subcategory_name=item_subcategory,
                    created_by_employee_id=session["employee_tin_number"],
                    item_description=item_description,
                    item_shelf_life=item_shelf_life)
                
                db.session.add(item)
                db.session.commit()
                return redirect("/dashboard")
            return render_template("item_registeration.html",db_location=db_location,db_unit=db_unit,db_currency=db_currency,db_category=db_category,db_subcategory=db_subcategory,sucess=True)
        else:
            return render_template("404.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/item_checkout",methods=["GET","POST"])
@login_required
def item_checkout():
    try:
        if session["department_name"]=="Store" or session["department_name"]=="Administration":
            if request.method=="POST":
                item_name=request.form["item_name"]
                return_employee_id=request.form["return_employee_id"]
                checkout_date=request.form["checkout_date"]
                item_quantity=request.form["item_quantity"]
                item_siv=request.form["item_siv"]
                item_status=request.form["item_status"]
                department=request.form["department"]
                location_name=request.form["location"]
                item_description=request.form["item_description"]
                unit_name=request.form["unit"]
                checkout_date = datetime.strptime(checkout_date, "%Y-%m-%d").date()

                item=db.session.query(Item).filter(Item.item_name==item_name).first()

                if item.item_quantity-float(item_quantity)<0:
                    return render_template("checkout.html",negative=True)

                stmt=(
                    update(
                        Item
                    ).where(Item.item_name==item_name)
                    .values(item_quantity=Item.item_quantity-float(item_quantity))
                )

                db.session.execute(stmt)
                db.session.commit()

                checkout_item=CheckOut(
                    item_name=item_name,return_employee_id=return_employee_id,checkout_date=checkout_date,
                    item_quantity=item_quantity,item_siv=item_siv,department=department,
                    location_name=location_name,item_description=item_description,item_status=item_status,
                    unit_name=unit_name,employee_tin_number=session["employee_tin_number"])
                db.session.add(checkout_item)
                db.session.commit()
                
            return render_template("checkout.html",item_name_list=item_name_list,db_location=db_location,db_unit=db_unit,db_department=db_department,sucess=True)
        else:
            return render_template("404.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/item_checkin",methods=["GET","POST"])
@login_required
def item_checkin():
    try:
        if session["department_name"]=="Store" or session["department_name"]=="Administration":
            item_name_list=db.session.query(Item.item_name).all()
            if request.method=="POST":
                item_name=request.form["item_name"]
                reciving_employee_id=request.form["reciving_employee_id"]
                checkin_date=request.form["checkin_date"]
                checkin_date = datetime.strptime(checkin_date, "%Y-%m-%d").date()
                item_price=request.form["item_price"]
                item_quantity=request.form["item_quantity"]
                item_grr=request.form["item_grr"]
                item_description=request.form["item_description"]
                unit=request.form["unit"]
                item_status=request.form["item_status"]
                currency=request.form["currency"]
                item_shelf_life=request.form["item_shelf_life"]
                item_shelf_life=datetime.strptime(item_shelf_life, "%Y-%m-%d").date()
                stmt=(
                    update(Item)
                    .where(Item.item_name==item_name)
                    .values(item_quantity=Item.item_quantity+int(item_quantity))
                )
                
                db.session.execute(stmt)
                db.session.commit()
                
                checkin_item=CheckIn(
                        item_name=item_name,reciving_employee_id=reciving_employee_id,
                        employee_tin_number=session["employee_tin_number"],item_price=item_price,
                        item_quantity=item_quantity,item_grr=item_grr,
                        item_description=item_description,unit_name=unit,
                        checkin_date=checkin_date,currency_name=currency,
                        item_shelf_life=item_shelf_life,item_status=item_status)

                
                db.session.add(checkin_item)
                db.session.commit()
                return render_template("checkin.html")
                        
            return render_template("checkin.html",item_name_list=item_name_list,db_currency=db_currency,db_unit=db_unit,)
        else:
            return render_template("404.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/customer_list")
@login_required
def customer_list():
    try:
        if session["Sales"]=="Human Resources" or session["department_name"]=="Administration":
            return render_template("customer_list.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/customer_list/list/<employee_tin_number>")
@login_required
def customer_list(employee_tin_number):
    try:
        if session["Sales"]=="Human Resources" or session["department_name"]=="Administration":
            customer_list_name=db.session.query(Customer).where(
                                Customer.regsistered_employee_tin_number==employee_tin_number
                            ).all()

            lst=[]

            for i in customer_list_name:
                lst.append(
                    {
                        "customer_tin":i[0],
                        "customer_name":i[1],
                        "customer_email":i[2],
                        "customer_phonenumber":i[3],
                        "customer_location":i[4]
                    }
                )


            return jsonify(lst)
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")


@app.route("/sales_registeration",methods=["GET","POST"])
@login_required
def sales_registeration():
    try:
        if session["department_name"]=="Sales" or session["department_name"]=="Administration":
            if request.method=="POST":
                item_name=request.form["item_name"]
                item_quantity=request.form["item_quantity"]
                item_price=request.form["item_price"]
                customer_tin=request.form["customer_tin"]
                unit_name=request.form["unit_name"]
                currency_name=request.form["currency_name"]
                
                item=db.session.query(Item).filter(Item.item_name==item_name).first()

                if item.item_quantity-int(item_quantity)<0:
                    return render_template("sales_registeration.html",negative=True,db_currency=db_currency,db_unit=db_unit)

                stmt=(
                    update(
                        Item
                    ).where(Item.item_name==item_name)
                    .values(item_quantity=Item.item_quantity-float(item_quantity))
                )

                db.session.execute(stmt)
                db.session.commit()

                sales=Sales(
                    item_name=item_name,item_quantity=item_quantity,item_price=item_price,
                    customer_tin=customer_tin,unit_name=unit_name,currency_name=currency_name,
                    employee_tin_number=session["employee_tin_number"]
                )

                db.session.add(sales)
                db.session.commit()
                return render_template("sales_registeration.html",item_name_list=item_name_list,sucess=True,db_currency=db_currency,db_unit=db_unit)

            return render_template("sales_registeration.html",item_name_list=item_name_list,db_currency=db_currency,db_unit=db_unit)
        else:
            return render_template("404.html")
        
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/purchase_order",methods=["GET","POST"])
@login_required
def purchase_order():
    try:
        if request.method=="POST":
            item_name=request.form["item_name"]
            ordered_quantity=request.form["ordered_quantity"]
            purchase_reason=request.form["purchase_reason"]
            order_status="Pending"
            purchase=PurchaseOrder(
                item_name=item_name,ordered_quantity=ordered_quantity,
                purchase_reason=purchase_reason,order_status=order_status,
                employee_tin_number=session["employee_tin_number"]
            )
            db.session.add(purchase)
            db.session.commit()
        return render_template("purchase_order.html",item_name_list=item_name_list,sucess=True)
    
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/customer_registeration",methods=["GET","POST"])
@login_required
def customer_registeration():
    try:
        if session["department_name"]=="Sales" or session["department_name"]=="Administration":
            if request.method=="POST":
                customer_name=request.form["customer_name"]
                customer_email=request.form["customer_email"]
                customer_phonenumber=request.form["customer_phonenumber"]
                customer_tin=request.form["customer_tin"]
                customer_location=request.form["customer_location"]
                
                
                customer=Customer(
                    customer_tin=customer_tin,customer_phonenumber=customer_phonenumber,
                    customer_name=customer_name,customer_location=customer_location,
                    customer_email=customer_email,regsistered_employee_tin_number=session["employee_tin_number"],
                   
                )
                
                db.session.add(customer)
                db.session.commit()
                return render_template("customer_registeration.html",db_location=db_location,sucess=True)

            return render_template("customer_registeration.html",db_location=db_location)
        else:
            return render_template("404.html")
        
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")
    
@app.route("/vendor_regsisteration",methods=["GET","POST"])
@login_required
def vendor_regsisteration():
    try:
        if session["department_name"]=="Procurement" or session["department_name"]=="Administration":
            if request.method=="POST":
                vendor_name=request.form["vendor_name"]
                vendor_tin=request.form["vendor_tin"]
                vendor_phonenumber=request.form["vendor_phonenumber"]
                vendor_email=request.form["vendor_email"]
                location=request.form["location"]
                item_name=request.form["item_name"]
                unit=request.form["unit"]
                item_quantity=request.form["item_quantity"]
                item_price=request.form["request.form"]

                vendor=Vendor(
                    vendor_name=vendor_name,vendor_tin=vendor_tin,
                    vendor_phonenumber=vendor_phonenumber,vendor_email=vendor_email,
                    location=location,item_name=item_name,unit=unit,
                    item_quantity=item_quantity,item_price=item_price
                )
                
                db.session.add(vendor)
                db.session.commit()
                return render_template("vendor_regsisteration.html",sucess=True)

            return render_template("vendor_regsisteration.html",db_unit=db_unit,item_name_list=item_name_list,db_location=db_location)
        else:
            return render_template("404.html")
        
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")
    
@app.route("/login",methods=["GET","POST"])
@limiter.limit("5 per minute")
def login():
    try:
        if "logged_in" in session and session["logged_in"]==True:
            return redirect("/dashboard")
        elif request.method=="POST":
            employee_tin_number=request.form["employee_id"]
            password=request.form["password"]
            employee=db.session.query(Employee).filter(Employee.employee_tin_number==employee_tin_number).first()
            is_vaild=bcrypt.checkpw(password.encode("utf-8"),employee.password)
            if is_vaild==True and employee.employment_status=="Active":
                login_user(employee)
                session["employee_tin_number"]=employee.employee_tin_number
                session["logged_in"]=True
                session["department_name"]=employee.department_name
                return redirect("/dashboard")
            return redirect("/login")
        return render_template("login.html")
    except Exception as e:
        logging.exception(str(e))
        db.session.rollback()
        return render_template("404.html")

@app.route("/logout")
def logout():
    try:
        logout_user()
        session.clear()
        return redirect("/login")
    except Exception as e:
        logging.exception(str(e))
        return render_template("404.html")

@app.route("/dashboard")
def dashboard():
    try:
        return render_template("hr_dashboard.html")
    except Exception as e:
        logging.exception(str(e))
        return render_template("404.html")
    

if __name__=="__main__":
    app.run(debug=True)