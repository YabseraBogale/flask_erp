from flask import Flask,url_for,render_template,redirect,request,session

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
        emergency_contact_gender=request.form["emergency_contact_gender"].value
        emergency_contact_phonenumber=request.form["emergency_contact_phonenumber"]
        emergency_contact_email=request.form["emergency_contact_email"]
        emergency_contact_location=request.form["emergency_contact_location"]

        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        middlename=request.form["middlename"]
        gender=request.form["gender"]
        phonenumber=request.form["phonenumber"]
        email=request.form["phonenumber"]
        date_of_employement=request.form["date_of_employement"]
        fyida_id=request.form["fyida_id"]
        position=request.form["position"]
        location=request.form["location"]
        department=request.form["department"]
        job_description=request.form["job_description"]
        tin_number=request.form["tin_number"]
        bank_account_number=request.form["bank_account_number"]
        salary=request.form["salary"]

        return "ok"
    return render_template("employee_registeration.html")


    
@app.route("/item_regsisteration.html",methods=["GET","POST"])
def item_registeration():
    if request.method=="POST":
        item_name=request.form["item_name"]
        item_price=request.form["item_price"]
        unit=request.form["unit"]
        created_by_employee_id=request.form["created_by_employee_id"]
        location=request.form["location"]
        item_category=request.form["item_category"]
        item_subcategory=request.form["item_subcategory"]
        item_quantity=request.form["item_quantity"]
        item_description=request.form["item_description"]
        item_name=request.form["item_name"]

        return "ok"
    return render_template("item_registeration.html")




@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(debug=True)