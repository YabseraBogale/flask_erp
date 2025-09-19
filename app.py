from flask import Flask,url_for,render_template,redirect,request,session

app=Flask(__name__)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(debug=True)