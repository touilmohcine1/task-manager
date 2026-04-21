"""
Categories Blueprint
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Category

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@categories_bp.route("/")
@login_required
def index():
    cats = Category.query.filter_by(user_id=current_user.id).all()
    return render_template("categories/index.html", categories=cats)


@categories_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name  = request.form.get("name", "").strip()
        color = request.form.get("color", "#6366f1")
        icon  = request.form.get("icon", "📁")

        if not name:
            flash("اسم التصنيف مطلوب", "error")
            return render_template("categories/form.html", category=None)

        cat = Category(name=name, color=color, icon=icon, user_id=current_user.id)
        db.session.add(cat)
        db.session.commit()
        flash("تم إنشاء التصنيف ✅", "success")
        return redirect(url_for("categories.index"))

    return render_template("categories/form.html", category=None)


@categories_bp.route("/<int:cat_id>/edit", methods=["GET", "POST"])
@login_required
def edit(cat_id):
    cat = Category.query.filter_by(id=cat_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        cat.name  = request.form.get("name", "").strip()
        cat.color = request.form.get("color", "#6366f1")
        cat.icon  = request.form.get("icon", "📁")
        db.session.commit()
        flash("تم تحديث التصنيف ✅", "success")
        return redirect(url_for("categories.index"))

    return render_template("categories/form.html", category=cat)


@categories_bp.route("/<int:cat_id>/delete", methods=["POST"])
@login_required
def delete(cat_id):
    cat = Category.query.filter_by(id=cat_id, user_id=current_user.id).first_or_404()
    db.session.delete(cat)
    db.session.commit()
    flash("تم حذف التصنيف", "info")
    return redirect(url_for("categories.index"))
