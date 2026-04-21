# ✅ Task Manager — Flask + MySQL + Python

نظام إدارة المهام مبني بـ Flask + MySQL + Nginx مع دعم Docker و Ubuntu VM.

---

## 📁 هيكل المشروع

```
task-manager/
├── backend/                    # Flask Application
│   ├── app/
│   │   ├── __init__.py         # App factory
│   │   ├── models.py           # SQLAlchemy models
│   │   └── routes/
│   │       ├── auth.py         # Login / Register
│   │       ├── dashboard.py    # Dashboard
│   │       ├── tasks.py        # Tasks CRUD
│   │       └── categories.py   # Categories CRUD
│   ├── run.py                  # Entry point
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # HTML + CSS + JS
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/               # login, register
│   │   ├── dashboard/
│   │   ├── tasks/
│   │   └── categories/
│   └── static/
│       ├── css/main.css
│       └── js/main.js
│
├── database/
│   └── schema.sql              # DB schema + seed data
│
├── docker/
│   └── nginx.conf              # Nginx for Docker
│
├── deployment/                 # Ubuntu VM deployment
│   ├── install.sh              # One-click installer
│   ├── nginx-taskmanager.conf  # Nginx for VM
│   └── systemd/
│       └── taskmanager.service # Systemd service
│
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

---

## 🐳 التشغيل بـ Docker (للتطوير والفهم)

### المتطلبات
- Docker Desktop أو Docker Engine
- Docker Compose

### الخطوات

```bash
# 1. استنسخ المشروع
git clone <repo-url> task-manager
cd task-manager

# 2. شغّل كل الخدمات دفعة واحدة
docker-compose up -d --build

# 3. افتح التطبيق
# http://localhost       ← عبر Nginx (المنفذ 80)
# http://localhost:5000  ← Flask مباشرة

# 4. عرض الـ Logs
docker-compose logs -f app
docker-compose logs -f db

# 5. إيقاف الخدمات
docker-compose down

# إيقاف مع حذف قاعدة البيانات
docker-compose down -v
```

### الخدمات في Docker Compose

| الخدمة  | الصورة          | المنفذ | الوصف               |
|---------|-----------------|--------|---------------------|
| db      | mysql:8.0       | 3306   | قاعدة بيانات MySQL  |
| app     | (Dockerfile)    | 5000   | Flask + Gunicorn    |
| nginx   | nginx:alpine    | 80     | Reverse Proxy       |

### لماذا نستخدم Docker؟
- **بيئة موحّدة**: نفس الإعدادات على كل جهاز
- **عزل الخدمات**: كل خدمة في حاوية منفصلة
- **سهولة التشغيل**: أمر واحد يشغّل كل شيء
- **مثالي للتطوير**: تغيير الكود ينعكس فوراً

---

## 🖥️ التثبيت على Ubuntu VM (الإنتاج)

### المتطلبات
- Ubuntu 22.04 LTS (أو 20.04)
- صلاحيات root / sudo
- اتصال بالإنترنت

### الطريقة السريعة (سطر واحد)

```bash
# انسخ المشروع على الـ VM
git clone <repo-url> /tmp/task-manager
cd /tmp/task-manager

# شغّل المثبّت
sudo bash deployment/install.sh
```

المثبّت يقوم تلقائياً بـ:
1. تحديث النظام
2. تثبيت Python 3, MySQL, Nginx, Git
3. إنشاء مستخدم نظام `taskmanager`
4. نسخ الملفات إلى `/opt/taskmanager`
5. إنشاء Python venv وتثبيت المكتبات
6. إعداد MySQL وتحميل الـ schema
7. كتابة ملف `.env`
8. تسجيل خدمة Systemd (**تبدأ تلقائياً عند إعادة التشغيل**)
9. إعداد Nginx كـ Reverse Proxy
10. إعداد UFW Firewall

---

### التثبيت اليدوي خطوة بخطوة

#### 1. تحديث النظام وتثبيت المتطلبات

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
    python3 python3-pip python3-venv \
    mysql-server nginx git curl \
    pkg-config libmysqlclient-dev build-essential
```

#### 2. إعداد MySQL

```bash
# تشغيل MySQL
sudo systemctl enable mysql --now

# إنشاء قاعدة البيانات والمستخدم
sudo mysql -u root <<SQL
CREATE DATABASE taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'taskuser'@'localhost' IDENTIFIED BY 'StrongPass123!';
GRANT ALL PRIVILEGES ON taskmanager.* TO 'taskuser'@'localhost';
FLUSH PRIVILEGES;
SQL

# تحميل الـ schema
mysql -u taskuser -p'StrongPass123!' taskmanager < database/schema.sql
```

#### 3. نسخ الملفات وإعداد Python

```bash
# نسخ المشروع
sudo cp -r . /opt/taskmanager
sudo useradd -r -s /bin/false taskmanager
sudo chown -R taskmanager:taskmanager /opt/taskmanager

# إنشاء Virtual Environment
sudo python3 -m venv /opt/taskmanager/venv
sudo /opt/taskmanager/venv/bin/pip install -r /opt/taskmanager/backend/requirements.txt
```

#### 4. ملف الإعدادات .env

```bash
sudo cp /opt/taskmanager/backend/.env.example /opt/taskmanager/backend/.env
sudo nano /opt/taskmanager/backend/.env
# عدّل: SECRET_KEY, DB_PASSWORD
```

#### 5. تثبيت Systemd Service

```bash
sudo cp /opt/taskmanager/deployment/systemd/taskmanager.service /etc/systemd/system/

# تفعيل الخدمة (تبدأ تلقائياً عند إعادة التشغيل)
sudo systemctl daemon-reload
sudo systemctl enable taskmanager
sudo systemctl start  taskmanager

# تحقق من الحالة
sudo systemctl status taskmanager
```

#### 6. إعداد Nginx

```bash
sudo cp /opt/taskmanager/deployment/nginx-taskmanager.conf \
         /etc/nginx/sites-available/taskmanager

sudo ln -sf /etc/nginx/sites-available/taskmanager \
             /etc/nginx/sites-enabled/taskmanager

sudo rm -f /etc/nginx/sites-enabled/default

# اختبر وأعِد تشغيل Nginx
sudo nginx -t
sudo systemctl reload nginx
```

#### 7. إعداد Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## 🔧 أوامر الإدارة (Ubuntu VM)

```bash
# ── حالة الخدمة ──────────────────────────────────────────
sudo systemctl status taskmanager

# ── إعادة تشغيل التطبيق ──────────────────────────────────
sudo systemctl restart taskmanager

# ── إيقاف / تشغيل ────────────────────────────────────────
sudo systemctl stop  taskmanager
sudo systemctl start taskmanager

# ── عرض Logs مباشرة ──────────────────────────────────────
sudo journalctl -u taskmanager -f

# ── Logs الملفات ─────────────────────────────────────────
tail -f /var/log/taskmanager/access.log
tail -f /var/log/taskmanager/error.log

# ── Nginx ────────────────────────────────────────────────
sudo systemctl status nginx
sudo nginx -t
sudo systemctl reload nginx

# ── MySQL ────────────────────────────────────────────────
sudo systemctl status mysql
mysql -u taskuser -p'StrongPass123!' taskmanager

# ── التحقق من التشغيل التلقائي (يجب أن يظهر enabled) ───
sudo systemctl is-enabled taskmanager
```

---

## ⚖️ مقارنة: Docker مقابل Ubuntu VM

| المعيار               | Docker                          | Ubuntu VM (Systemd)         |
|----------------------|---------------------------------|-----------------------------|
| **سهولة التشغيل**   | `docker-compose up` واحدة      | تثبيت خطوة بخطوة           |
| **عزل البيئة**      | ✅ كامل (containers)            | ⚠️ جزئي (venv فقط)         |
| **الأداء**           | ⚠️ overhead بسيط               | ✅ أداء أفضل (native)       |
| **التحديث**          | إعادة بناء الصورة              | `git pull` + restart        |
| **التشغيل التلقائي** | `restart: always`               | `systemctl enable`          |
| **Logs**             | `docker logs`                   | `journalctl`                |
| **مناسب لـ**         | التطوير، CI/CD                  | خوادم الإنتاج البسيطة      |

---

## 🌐 بنية النظام

```
المستخدم
    │
    ▼ HTTP :80
┌─────────┐
│  Nginx  │  ← Reverse Proxy / Static Files
└────┬────┘
     │
     ▼ :5000 (localhost فقط)
┌──────────┐
│ Gunicorn │  ← Python WSGI Server (2 workers)
│  Flask   │  ← Business Logic
└────┬─────┘
     │
     ▼ :3306 (localhost فقط)
┌─────────┐
│  MySQL  │  ← قاعدة البيانات
└─────────┘
```

---

## 🔒 الأمان

- Flask يعمل على `127.0.0.1` (غير مكشوف للخارج)
- MySQL يعمل على `localhost` فقط
- Nginx هو المدخل الوحيد من الخارج
- `.env` محمي بصلاحيات `640`
- مستخدم نظام منفصل بدون shell

---

## 🐛 حل المشاكل الشائعة

```bash
# التطبيق لا يعمل
sudo systemctl status taskmanager
sudo journalctl -u taskmanager -n 50

# خطأ في الاتصال بـ MySQL
mysql -u taskuser -p'StrongPass123!' -h localhost taskmanager

# Nginx لا يعمل
sudo nginx -t
sudo journalctl -u nginx -n 20

# إعادة تعيين قاعدة البيانات
mysql -u taskuser -p'StrongPass123!' taskmanager < /opt/taskmanager/database/schema.sql
```
#   t a s k - m a n a g e r  
 