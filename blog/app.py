from flask import Flask, render_template, request, redirect, url_for, session
from userdb import UserDB

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route("/")
def home():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    users_db = UserDB()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_db.get_user(username)
        if user and user[2] == password:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    users_db = UserDB()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_db.get_user(username)
        if user:
            return render_template("register.html", error="Username already exists")
        users_db.create_user(username, password)
        session["username"] = username
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)

