from flask import Flask,url_for,render_template,redirect,request,session

from database import db,EmergencyContact,Employee,Item,ItemLog,TransactionType,Checkout


app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.add(TransactionType(type_name="add"))
    db.session.add(TransactionType(type_name="remove"))
    db.session.add(TransactionType(type_name="transfer"))
    db.session.commit()
    
    



@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(debug=True)