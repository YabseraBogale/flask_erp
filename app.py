from flask import Flask,url_for,render_template,redirect,request,session
from datetime import datetime
from database import db,EmergencyContact,Employee,Item,ItemLog,TransactionType,Checkout


app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
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
        
        db.session.add(emergency_contact)
        db.session.commit()

        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        middlename=request.form["middlename"]
        gender=request.form["gender"]
        phonenumber="+251 "+request.form["phonenumber"]
        email=request.form["phonenumber"]
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

        employee=Employee(emergency_contact_fyida_id=emergency_contact_fyida_id,
                        firstname=firstname,lastname=lastname,middlename=middlename,phonenumber=phonenumber,
                        gender=gender,email=email,date_of_employement=date_of_employement,fyida_id=fyida_id,
                        position=position,location=location,department=department,job_description=job_description,
                        tin_number=tin_number,bank_account_number=bank_account_number,salary=salary
                        )
        
        db.session.add(employee)
        db.session.commit()

        return "ok"
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

        item=Item(item_name=item_name,item_price=item_price,
                  item_quantity=item_quantity,unit=unit,category=item_category,
                  location=location,subcategory=item_subcategory,
                  created_by_employee_id=1,item_description=item_description
                )
        
        db.session.add(item)
        db.session.commit()

        return "ok"
    return render_template("item_regsisteration.html")

@app.route("/item_add",methods=["GET","POST"])
def item_add():
    if request.method=="POST":
        item_id=request.form["item_id"]
        item_price=request.form["item_price"]
        quantity_changed=request.form["item_quantity"]
        transaction_type_name="add"
        transaction_date=datetime.today()
        description=request.form["description"]

        itemlog=ItemLog(
            item_id=item_id,
            item_price=item_price,
            quantity_changed=quantity_changed,
            transaction_type_name=transaction_type_name,
            transaction_date=transaction_date,
            description=description
        )

        # in item
        # update item price with change only.
        # item qunquantity with the pervious plus the add quantity
        # update the description

        return "ok"
    return render_template("item_add.html")


@app.route("/item_checkout",methods=["GET","POST"])
def item_checkout():
    pass

@app.route("/item_checkin",methods=["GET","POST"])
def item_checkin():
    pass



@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(debug=True)