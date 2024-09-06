from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
)

# إعداد التطبيق
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# نموذج المستخدم
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


# تحميل المستخدم
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


# التسجيل
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(
            username=request.form.get("username"), password=request.form.get("password")
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")


# تسجيل الدخول
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user and user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")


# تسجيل الخروج
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


# الصفحة الرئيسية
@app.route("/")
@login_required
def home():
    return render_template("home.html")


# تشغيل التطبيق
if __name__ == "__main__":
    app.run()
