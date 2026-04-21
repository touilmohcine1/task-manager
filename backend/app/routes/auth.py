"""
Auth Blueprint — Login / Register / Logout
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Category

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.index"))

        flash("البريد الإلكتروني أو كلمة المرور غير صحيحة", "error")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if password != confirm:
            flash("كلمات المرور غير متطابقة", "error")
            return render_template("auth/register.html")

        if User.query.filter_by(email=email).first():
            flash("البريد الإلكتروني مستخدم بالفعل", "error")
            return render_template("auth/register.html")

        if User.query.filter_by(username=username).first():
            flash("اسم المستخدم مستخدم بالفعل", "error")
            return render_template("auth/register.html")

        user = User(username=username, email=email, avatar="🧑‍💻")
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        # Default categories for new user
        defaults = [
            Category(name="العمل",    color="#6366f1", icon="💼", user_id=user.id),
            Category(name="شخصية",   color="#ec4899", icon="🏠", user_id=user.id),
            Category(name="تعلم",    color="#f59e0b", icon="📚", user_id=user.id),
            Category(name="صحة",     color="#10b981", icon="💪", user_id=user.id),
        ]
        db.session.add_all(defaults)
        db.session.commit()

        login_user(user)
        flash("مرحباً بك! تم إنشاء حسابك بنجاح", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج بنجاح", "success")
    return redirect(url_for("auth.login"))
