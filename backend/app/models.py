"""
Task Manager — SQLAlchemy Models
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(50),  unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    avatar     = db.Column(db.String(10),  default="👤")
    created_at = db.Column(db.DateTime,    default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,    default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks      = db.relationship("Task",     backref="owner",    lazy=True, cascade="all, delete-orphan")
    categories = db.relationship("Category", backref="owner",    lazy=True, cascade="all, delete-orphan")

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def to_dict(self):
        return {
            "id":         self.id,
            "username":   self.username,
            "email":      self.email,
            "avatar":     self.avatar,
            "created_at": self.created_at.isoformat(),
        }


class Category(db.Model):
    __tablename__ = "categories"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(50), nullable=False)
    color      = db.Column(db.String(7),  default="#6366f1")
    icon       = db.Column(db.String(10), default="📁")
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks      = db.relationship("Task", backref="category", lazy=True)

    def to_dict(self):
        return {
            "id":    self.id,
            "name":  self.name,
            "color": self.color,
            "icon":  self.icon,
            "tasks_count": len(self.tasks),
        }


class Task(db.Model):
    __tablename__ = "tasks"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status      = db.Column(db.Enum("todo", "in_progress", "done"), default="todo")
    priority    = db.Column(db.Enum("low", "medium", "high"),       default="medium")
    due_date    = db.Column(db.Date)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"),     nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    STATUS_LABELS = {
        "todo":        "قيد الانتظار",
        "in_progress": "جارٍ التنفيذ",
        "done":        "مكتملة",
    }
    PRIORITY_LABELS = {
        "low":    "منخفضة",
        "medium": "متوسطة",
        "high":   "عالية",
    }

    def to_dict(self):
        return {
            "id":           self.id,
            "title":        self.title,
            "description":  self.description,
            "status":       self.status,
            "status_label": self.STATUS_LABELS.get(self.status, self.status),
            "priority":     self.priority,
            "priority_label": self.PRIORITY_LABELS.get(self.priority, self.priority),
            "due_date":     self.due_date.isoformat() if self.due_date else None,
            "category_id":  self.category_id,
            "category":     self.category.to_dict() if self.category else None,
            "created_at":   self.created_at.isoformat(),
            "updated_at":   self.updated_at.isoformat(),
        }
