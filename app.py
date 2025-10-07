import smtplib
import os
import string
import random
import bcrypt
from flask import Flask,url_for,render_template,redirect,request,session
from datetime import datetime
from sqlalchemy.exc import IntegrityError, OperationalError
from database import db,EmergencyContact,Employee,Item,CheckOut,CheckIn
from email.message import EmailMessage
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



app=Flask(__name__)


company_email=os.getenv("company_email")
company_email_password=os.getenv("company_email_password")



salt = bcrypt.gensalt()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY']=os.getenv("SECRET_KEY")

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://sqlite:///database.db",
)

db.init_app(app)

with app.app_context():
    db.create_all()
    
    

@app.route("/employee_registeration",methods=["GET","POST"])
def employee_registeration():
    
    if request.method=="POST":
        emergency_contact_fyida_id=request.form["emergency_contact_fyida_id"]
        emergency_contact_firstname=request.form["emergency_contact_firstname"]
        emergency_contact_lastname=request.form["emergency_contact_lastname"]
        emergency_contact_middlename=request.form["emergency_contact_middlename"]
        emergency_contact_gender=request.form["emergency_contact_gender"]
        emergency_contact_phonenumber="+251 "+request.form["emergency_contact_phonenumber"]
        emergency_contact_email=request.form["emergency_contact_email"]
        emergency_contact_location=request.form["emergency_contact_location"]

        emergency_contact=EmergencyContact(firstname=emergency_contact_firstname,
                                           lastname=emergency_contact_lastname,middlename=emergency_contact_middlename,
                                           phonenumber=emergency_contact_phonenumber,location=emergency_contact_location,
                                           fyida_id=emergency_contact_fyida_id,gender=emergency_contact_gender,
                                           email=emergency_contact_email
                                           )
        try:

            db.session.add(emergency_contact)
            db.session.commit()

        except IntegrityError as e:
            
            if "emergency_contact_email" in str(e) and "fyida_id" in str(e):
                return render_template("employee_registeration.html",emergency_email=True,emergency_id=True)
            elif "emergency_contact_email" in str(e):
                return render_template("employee_registeration.html",emergency_email=True)
            elif "fyida_id" in str(e):
                return render_template("employee_registeration.html",emergency_id=True)
        

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
        salary=request.form["salary"]
        characters = string.ascii_letters + string.digits + string.punctuation
        password_to_send = ''.join(random.choice(characters) for i in range(15))
        
        

        password=(password_to_send).encode("utf-8")
        employee=Employee(emergency_contact_fyida_id=emergency_contact_fyida_id,
                        firstname=firstname,lastname=lastname,middlename=middlename,phonenumber=phonenumber,
                        gender=gender,email=email,date_of_employement=date_of_employement,fyida_id=fyida_id,
                        position=position,location=location,department=department,job_description=job_description,
                        tin_number=tin_number,bank_account_number=bank_account_number,salary=salary,password=bcrypt.hashpw(password,salt)
                        )
        
        try:
            db.session.add(employee)
            db.session.commit()

            employee=db.session.query(Employee).filter(Employee.email==email).first()
            subject="Well Come to Comapny Name"
            body=f"This sent by bot for Comapny Name password.Employee id:{employee.employee_id}  Your password: {password_to_send}"
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
                return render_template("employee_registeration.html")

            return redirect("/dashboard")
        
        except IntegrityError as e:
            return render_template("employee_registeration.html")
        
    return render_template("employee_registeration.html")



    
@app.route("/item_regsisteration",methods=["GET","POST"])
def item_registeration():
    if request.method=="POST":
        item_name=request.form["item_name"]
        item_price=request.form["item_price"]
        unit=request.form["unit"]
        location=request.form["location"]
        item_category=request.form["item_category"]
        item_subcategory=request.form["item_subcategory"]
        item_quantity=request.form["item_quantity"]
        item_description=request.form["item_description"]
        item_name=request.form["item_name"]
        item_shelf_life=request.form["item_shelf_life"]
        item_shelf_life = datetime.strptime(item_shelf_life, "%Y-%m-%d").date()
        item=Item(
            item_name=item_name,item_price=item_price,
            item_quantity=item_quantity,unit=unit,category=item_category,
            location=location,subcategory=item_subcategory,
            created_by_employee_id=1,item_description=item_description,item_shelf_life=item_shelf_life)
        

        try:
            db.session.add(item)
            db.session.commit()
            return redirect("/dashboard")
        except IntegrityError as e:
            return render_template("item_registeration.html",msg="Item is already regisitered")
    return render_template("item_registeration.html")




@app.route("/item_checkout",methods=["GET","POST"])
def item_checkout():
    if request.method=="POST":
        item_name=request.form["item_name"]
        return_employee_id=request.form["return_employee_id"]
        checkout_date=request.form["checkout_date"]
        item_price=request.form["item_price"]
        item_quantity=request.form["item_quantity"]
        item_siv=request.form["item_siv"]
        department=request.form["department"]
        location=request.form["location"]
        item_description=request.form["item_description"]
        unit=request.form["unit"]
        checkout_date = datetime.strptime(checkout_date, "%Y-%m-%d").date()
        checkout_item=CheckOut(
            item_name=item_name,return_employee_id=return_employee_id,checkout_date=checkout_date,
            item_price=item_price,item_quantity=item_quantity,item_siv=item_siv,department=department,
            location=location,item_description=item_description,unit=unit
        )

        try:
            db.session.add(checkout_item)
            db.session.commit()
        
        except IntegrityError as e:
            return render_template("checkout.html")        

    return render_template("checkout.html")



@app.route("/item_checkin",methods=["GET","POST"])
def item_checkin():
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

        checkin_item=CheckIn(
            item_name=item_name,reciving_employee_id=reciving_employee_id,
            employee_id=session["employee_id"],item_price=item_price,item_quantity=item_quantity,
            item_grr=item_grr,item_description=item_description,unit=unit,checkin_date=checkin_date
        )

        try:
            db.session.add(checkin_item)
            db.session.commit()
            return render_template("checkin.html")
        
        except IntegrityError as e:
            return render_template("checkin.html")
        
    return render_template("checkin.html")



@app.route("/login",methods=["GET","POST"])
@limiter.limit("5 per minute")
def login():
    if request.method=="POST":
        employee_id=request.form["employee_id"]
        password=request.form["password"]
        employee=db.session.query(Employee).filter(Employee.employee_id==employee_id).first()
        is_vaild=bcrypt.checkpw(password.encode("utf-8"),employee.password)
        if is_vaild==True:
            session["employee_id"]=employee.employee_id
            session["logged_in"]=True
            session["department"]=employee.department
            return redirect("/dashboard")
        return redirect("/login")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("employee_id",None)
    session.pop("logged_in",None)
    session.pop("department",None)
    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    return render_template("hr_dashboard.html")

if __name__=="__main__":
    app.run(debug=True)