"""
Tasks Blueprint — Full CRUD
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Task, Category
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("/")
@login_required
def index():
    status   = request.args.get("status")
    priority = request.args.get("priority")
    cat_id   = request.args.get("category")

    query = Task.query.filter_by(user_id=current_user.id)
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if cat_id:
        query = query.filter_by(category_id=int(cat_id))

    tasks      = query.order_by(Task.created_at.desc()).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()

    return render_template("tasks/index.html", tasks=tasks, categories=categories,
                           current_status=status, current_priority=priority, current_category=cat_id,
                           now=datetime)


@tasks_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    categories = Category.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        title       = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status      = request.form.get("status", "todo")
        priority    = request.form.get("priority", "medium")
        due_date    = request.form.get("due_date")
        cat_id      = request.form.get("category_id") or None

        if not title:
            flash("عنوان المهمة مطلوب", "error")
            return render_template("tasks/form.html", categories=categories, task=None)

        task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            user_id=current_user.id,
            category_id=int(cat_id) if cat_id else None,
        )
        if due_date:
            task.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

        db.session.add(task)
        db.session.commit()
        flash("تم إنشاء المهمة بنجاح ✅", "success")
        return redirect(url_for("tasks.index"))

    return render_template("tasks/form.html", categories=categories, task=None)


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    categories = Category.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        task.title       = request.form.get("title", "").strip()
        task.description = request.form.get("description", "").strip()
        task.status      = request.form.get("status", "todo")
        task.priority    = request.form.get("priority", "medium")
        cat_id           = request.form.get("category_id") or None
        task.category_id = int(cat_id) if cat_id else None
        due_date         = request.form.get("due_date")
        task.due_date    = datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else None

        db.session.commit()
        flash("تم تحديث المهمة بنجاح ✅", "success")
        return redirect(url_for("tasks.index"))

    return render_template("tasks/form.html", categories=categories, task=task)


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash("تم حذف المهمة", "info")
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/<int:task_id>/status", methods=["POST"])
@login_required
def update_status(task_id):
    """Quick status toggle via AJAX"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    new_status = data.get("status")
    if new_status in ("todo", "in_progress", "done"):
        task.status = new_status
        db.session.commit()
        return jsonify({"success": True, "status": task.status})
    return jsonify({"success": False}), 400


# ── API endpoints (JSON) ──────────────────────────────────────
@tasks_bp.route("/api/list")
@login_required
def api_list():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])
