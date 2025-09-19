from flask import Flask,url_for,render_template,redirect,request,session

from database import db


app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(debug=True)