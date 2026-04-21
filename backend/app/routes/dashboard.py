"""
Dashboard Blueprint
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Task, Category
from datetime import date

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def index():
    tasks      = Task.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()

    today = date.today()
    stats = {
        "total":       len(tasks),
        "todo":        sum(1 for t in tasks if t.status == "todo"),
        "in_progress": sum(1 for t in tasks if t.status == "in_progress"),
        "done":        sum(1 for t in tasks if t.status == "done"),
        "overdue":     sum(1 for t in tasks if t.due_date and t.due_date < today and t.status != "done"),
        "high":        sum(1 for t in tasks if t.priority == "high" and t.status != "done"),
    }

    recent_tasks = (
        Task.query.filter_by(user_id=current_user.id)
        .order_by(Task.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/index.html",
        stats=stats,
        recent_tasks=recent_tasks,
        categories=categories,
    )
