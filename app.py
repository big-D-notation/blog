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
            return redirect(url_for("profile"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    users_db = UserDB()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]  # Added email field
        user = users_db.get_user(username)
        if user:
            return render_template("register.html", error="Username already exists")
        users_db.create_user(username, password, email)  # Updated create_user method
        session["username"] = username
        return redirect(url_for("profile"))
    return render_template("register.html")


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    users_db = UserDB()

    if request.method == "POST":
        username = request.form["username"]
        new_password = request.form["new_password"]
        user = users_db.get_user(username)
        if user:
            users_db.update_password(username, new_password)
            return redirect(url_for("login"))
        else:
            return render_template("reset_password.html", error="Invalid username")
    return render_template("reset_password.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    if "username" in session:
        users_db = UserDB()

        if request.method == "POST":
            username = session["username"]
            title = request.form["title"]
            content = request.form["content"]

            users_db.add_post(username, title, content)
            return redirect(url_for("profile"))

        return render_template("add_post.html")
    return redirect(url_for("login"))


@app.route("/add_comment/<int:post_id>", methods=["GET", "POST"])
def add_comment(post_id):
    if "username" in session:
        users_db = UserDB()

        if request.method == "POST":
            username = session["username"]
            comment = request.form["comment"]

            users_db.add_comment(post_id, username, comment)
            return redirect(url_for("profile"))

        return render_template("add_comment.html", post_id=post_id)
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if "username" in session:
        username = session["username"]
        users_db = UserDB()

        user_posts = users_db.get_user_posts(username)
        print(user_posts)

        return render_template("profile.html", username=username, user_posts=user_posts)
    return redirect(url_for("login"))


@app.route("/profile/<username>")
def stranger_profile(username):
    if "username" in session:
        this_username = session["username"]
        users_db = UserDB()

        user_posts = users_db.get_user_posts(username)
        print(user_posts)

        return render_template("stranger_profile.html", this_username=this_username, username=username, user_posts=user_posts)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
    