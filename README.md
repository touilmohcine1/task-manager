# 📋 Task Manager - نظام إدارة المهام

<div align="center">

**نظام إدارة مهام متقدم مبني بـ Flask + MySQL + Python**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](docker-compose.yml)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](#)

[الميزات](#-الميزات) • [الثبت](#-التثبيت) • [الاستخدام](#-الاستخدام) • [النشر](#-النشر)

</div>

---

## 📖 جدول المحتويات

1. [🎯 نظرة عامة](#-نظرة-عامة)
2. [✨ الميزات](#-الميزات)
3. [🛠️ التقنيات المستخدمة](#%EF%B8%8F-التقنيات-المستخدمة)
4. [📁 هيكل المشروع](#-هيكل-المشروع)
5. [🐳 التشغيل بـ Docker](#-التشغيل-بـ-docker)
6. [🖥️ التثبيت على Ubuntu](#%EF%B8%8F-التثبيت-على-ubuntu-vm)
7. [🔧 أوامر الإدارة](#-أوامر-الإدارة)
8. [🌐 بنية النظام](#-بنية-النظام)
9. [🔒 الأمان](#-الأمان)
10. [🐛 حل المشاكل](#-حل-المشاكل-الشائعة)
11. [📝 الملفات الهامة](#-الملفات-الهامة)
12. [📞 الدعم والمساهمة](#-الدعم-والمساهمة)

---

## 🎯 نظرة عامة

**Task Manager** هو نظام متكامل لإدارة المهام والمشاريع يوفر:
- ✅ إدارة المهام بكفاءة عالية
- 📂 تنظيم المهام بفئات منظمة
- 👤 نظام المستخدمين (تسجيل دخول/تسجيل جديد)
- 📊 لوحة تحكم شاملة وسهلة الاستخدام
- 🔐 أمان عالي المستوى

---

## ✨ الميزات

- **واجهة استخدام حديثة**: HTML5 + CSS3 + JavaScript
- **قاعدة بيانات قوية**: MySQL 8.0 مع دعم UTF-8
- **توازن الأحمال**: Nginx كـ Reverse Proxy
- **سهولة النشر**: Docker + Docker Compose + Systemd
- **مرن ومتقدم**: يعمل على التطوير والإنتاج بسهولة
- **آمن جداً**: تشفير كامل والاتصالات المحمية

---

## 🛠️ التقنيات المستخدمة

| الطبقة | التقنية |
|------|---------|
| **الواجهة الأمامية** | HTML5, CSS3, JavaScript |
| **الخادم** | Flask (Python 3.8+) |
| **قاعدة البيانات** | MySQL 8.0 |
| **خادم الويب** | Nginx + Gunicorn |
| **التكامل** | Docker & Docker Compose |
| **النشر** | Systemd & Nginx |

---

## 📁 هيكل المشروع

```
task-manager/
├── backend/                    # تطبيق Flask
│   ├── app/
│   │   ├── __init__.py         # App factory
│   │   ├── models.py           # نماذج SQLAlchemy
│   │   └── routes/             # مسارات التطبيق
│   │       ├── auth.py         # تسجيل الدخول والتسجيل
│   │       ├── dashboard.py    # لوحة التحكم
│   │       ├── tasks.py        # عمليات المهام CRUD
│   │       └── categories.py   # عمليات الفئات CRUD
│   ├── run.py                  # نقطة البداية
│   ├── requirements.txt        # مكتبات Python
│   └── .env.example            # ملف الإعدادات النموذجي
│
├── frontend/                   # HTML + CSS + JavaScript
│   ├── templates/              # قوالب HTML
│   │   ├── base.html          # القالب الأساسي
│   │   ├── auth/              # صفحات المصادقة
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard/         # صفحة لوحة التحكم
│   │   ├── tasks/             # صفحات المهام
│   │   └── categories/        # صفحات الفئات
│   └── static/                # الملفات الثابتة
│       ├── css/main.css       # أنماط CSS
│       └── js/main.js         # سكريبتات JavaScript
│
├── database/
│   └── schema.sql             # هيكل قاعدة البيانات وبيانات البذر
│
├── docker/
│   └── nginx.conf             # إعدادات Nginx للـ Docker
│
├── deployment/                # ملفات النشر على Ubuntu
│   ├── install.sh             # سكريبت التثبيت التلقائي
│   ├── nginx-taskmanager.conf # إعدادات Nginx للخادم
│   └── systemd/
│       └── taskmanager.service # خدمة Systemd
│
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

---

## 🐳 التشغيل بـ Docker

### المتطلبات
- Docker Desktop أو Docker Engine
- Docker Compose
- اتصال بالإنترنت

### الخطوات السريعة

```bash
# 1. استنسخ المشروع
git clone <repo-url> task-manager
cd task-manager

# 2. شغّل كل الخدمات دفعة واحدة
docker-compose up -d --build

# 3. افتح التطبيق في المتصفح
# عبر Nginx (المنفذ 80):        http://localhost
# Flask مباشرة (المنفذ 5000):   http://localhost:5000

# 4. عرض السجلات
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
- **بيئة موحّدة**: نفس الإعدادات على كل الأجهزة
- **عزل الخدمات**: كل خدمة في حاوية منفصلة
- **سهولة التشغيل**: أمر واحد يشغّل كل شيء
- **مثالي للتطوير**: تغيير الكود ينعكس فوراً

---

## 🖥️ التثبيت على Ubuntu VM

### المتطلبات
- Ubuntu 22.04 LTS (أو 20.04)
- صلاحيات root / sudo
- اتصال بالإنترنت

### الطريقة السريعة (سطر واحد)

```bash
# انسخ المشروع على الـ VM
git clone <repo-url> /tmp/task-manager
cd /tmp/task-manager

# شغّل المثبّت التلقائي
sudo bash deployment/install.sh
```

المثبّت يقوم تلقائياً بـ:
1. ✅ تحديث النظام
2. ✅ تثبيت Python 3, MySQL, Nginx, Git
3. ✅ إنشاء مستخدم نظام `taskmanager`
4. ✅ نسخ الملفات إلى `/opt/taskmanager`
5. ✅ إنشاء Python venv وتثبيت المكتبات
6. ✅ إعداد MySQL وتحميل الـ schema
7. ✅ كتابة ملف `.env`
8. ✅ تسجيل خدمة Systemd (**تبدأ تلقائياً عند إعادة التشغيل**)
9. ✅ إعداد Nginx كـ Reverse Proxy
10. ✅ إعداد UFW Firewall

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

#### 2. إعداد قاعدة البيانات MySQL

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

#### 3. نسخ الملفات وإعداد بيئة Python

```bash
# نسخ المشروع
sudo cp -r . /opt/taskmanager
sudo useradd -r -s /bin/false taskmanager
sudo chown -R taskmanager:taskmanager /opt/taskmanager

# إنشاء Virtual Environment
sudo python3 -m venv /opt/taskmanager/venv
sudo /opt/taskmanager/venv/bin/pip install -r /opt/taskmanager/backend/requirements.txt
```

#### 4. إعداد ملف الإعدادات .env

```bash
sudo cp /opt/taskmanager/backend/.env.example /opt/taskmanager/backend/.env
sudo nano /opt/taskmanager/backend/.env
# عدّل: SECRET_KEY, DB_PASSWORD, وغيرها
```

#### 5. تثبيت خدمة Systemd

```bash
sudo cp /opt/taskmanager/deployment/systemd/taskmanager.service /etc/systemd/system/

# تفعيل الخدمة (تبدأ تلقائياً عند إعادة التشغيل)
sudo systemctl daemon-reload
sudo systemctl enable taskmanager
sudo systemctl start  taskmanager

# تحقق من الحالة
sudo systemctl status taskmanager
```

#### 6. إعداد Nginx كـ Reverse Proxy

```bash
sudo cp /opt/taskmanager/deployment/nginx-taskmanager.conf \
         /etc/nginx/sites-available/taskmanager

sudo ln -sf /etc/nginx/sites-available/taskmanager \
             /etc/nginx/sites-enabled/taskmanager

# إزالة الإعدادات الافتراضية
sudo rm -f /etc/nginx/sites-enabled/default

# اختبر وأعِد تشغيل Nginx
sudo nginx -t
sudo systemctl reload nginx
```

#### 7. إعداد جدار الحماية (Firewall)

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## 🔧 أوامر الإدارة (Ubuntu VM)

### حالة الخدمة والتحكم بها

```bash
# عرض حالة الخدمة
sudo systemctl status taskmanager

# إعادة تشغيل التطبيق
sudo systemctl restart taskmanager

# إيقاف / تشغيل الخدمة
sudo systemctl stop  taskmanager
sudo systemctl start taskmanager

# التحقق من التشغيل التلقائي
sudo systemctl is-enabled taskmanager
```

### عرض السجلات (Logs)

```bash
# عرض Logs مباشرة من Systemd
sudo journalctl -u taskmanager -f

# عرض آخر 50 سطر
sudo journalctl -u taskmanager -n 50

# Logs الملفات
tail -f /var/log/taskmanager/access.log
tail -f /var/log/taskmanager/error.log
```

### إدارة Nginx

```bash
# عرض حالة Nginx
sudo systemctl status nginx

# اختبار الإعدادات
sudo nginx -t

# إعادة تحميل الإعدادات
sudo systemctl reload nginx

# عرض Logs
sudo journalctl -u nginx -n 20
```

### إدارة قاعدة البيانات

```bash
# عرض حالة MySQL
sudo systemctl status mysql

# الاتصال بقاعدة البيانات
mysql -u taskuser -p'StrongPass123!' -h localhost taskmanager

# عمل Backup
mysqldump -u taskuser -p'StrongPass123!' taskmanager > backup.sql

# استعادة Backup
mysql -u taskuser -p'StrongPass123!' taskmanager < backup.sql
```

---

## ⚖️ مقارنة: Docker مقابل Ubuntu VM

| المعيار               | Docker                          | Ubuntu VM (Systemd)         |
|----------------------|---------------------------------|-----------------------------|
| **سهولة التشغيل**   | `docker-compose up` أمر واحد   | تثبيت خطوة بخطوة            |
| **عزل البيئة**      | ✅ عزل كامل (containers)        | ⚠️ عزل جزئي (venv فقط)     |
| **الأداء**           | ⚠️ overhead بسيط               | ✅ أداء أفضل (native)      |
| **التحديث**          | إعادة بناء الصورة              | `git pull` + restart        |
| **التشغيل التلقائي** | `restart: always`              | `systemctl enable`          |
| **عرض السجلات**      | `docker logs`                  | `journalctl`                |
| **مناسب لـ**         | التطوير، CI/CD، الاختبار        | خوادم الإنتاج البسيطة      |

---

## 🌐 بنية النظام

```
┌─────────────────────────────────────────────────┐
│           المستخدم (على المتصفح)              │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼ HTTP :80
         ┌──────────────────────┐
         │      Nginx           │  ← Reverse Proxy
         │   Static Files       │     Load Balancer
         └──────────────┬───────┘
                        │
                        ▼ :5000 (localhost فقط)
         ┌──────────────────────┐
         │  Gunicorn (2 workers)│  ← Python WSGI Server
         │  Flask Application   │     Business Logic
         │  Request Handling    │
         └──────────────┬───────┘
                        │
                        ▼ :3306 (localhost فقط)
         ┌──────────────────────┐
         │      MySQL 8.0       │  ← قاعدة البيانات
         │   Data Persistence  │
         │   User/Tasks Data    │
         └──────────────────────┘
```

---

## 🔒 الأمان

- **Flask**: يعمل على `127.0.0.1` فقط (غير مكشوف للإنترنت)
- **MySQL**: يعمل على `localhost` فقط (بدون وصول خارجي)
- **Nginx**: هو المدخل الوحيد من الخارج (Reverse Proxy)
- **ملفات الإعدادات**: محمية بصلاحيات `640` (آمنة)
- **مستخدم النظام**: منفصل بدون shell (حماية إضافية)
- **كلمات المرور**: قوية ومشفرة (best practices)

---

## 🐛 حل المشاكل الشائعة

### المشكلة: التطبيق لا يعمل

```bash
# اعرض حالة الخدمة
sudo systemctl status taskmanager

# اعرض آخر 50 سطر من السجلات
sudo journalctl -u taskmanager -n 50
```

### المشكلة: خطأ في الاتصال بـ MySQL

```bash
# اختبر الاتصال بقاعدة البيانات
mysql -u taskuser -p'StrongPass123!' -h localhost taskmanager

# تحقق من حالة MySQL
sudo systemctl status mysql

# أعد تشغيل MySQL
sudo systemctl restart mysql
```

### المشكلة: Nginx لا يعمل

```bash
# اختبر إعدادات Nginx
sudo nginx -t

# عرض سجلات Nginx
sudo journalctl -u nginx -n 20

# أعد تشغيل Nginx
sudo systemctl restart nginx
```

### المشكلة: إعادة تعيين قاعدة البيانات

```bash
# احذف البيانات الحالية وأعد التحميل
mysql -u taskuser -p'StrongPass123!' taskmanager < /opt/taskmanager/database/schema.sql
```

---

## 📝 الملفات الهامة

| الملف | الموقع | الوصف |
|------|--------|-------|
| `docker-compose.yml` | الجذر | تكوين Docker Compose لجميع الخدمات |
| `Dockerfile` | الجذر | صورة Docker للتطبيق الرئيسي |
| `requirements.txt` | backend/ | قائمة مكتبات Python المطلوبة |
| `schema.sql` | database/ | هيكل قاعدة البيانات والبيانات الأولية |
| `install.sh` | deployment/ | سكريبت التثبيت التلقائي على Ubuntu |
| `.env.example` | backend/ | ملف الإعدادات النموذجي |
| `nginx.conf` | docker/ | إعدادات Nginx للـ Docker |
| `nginx-taskmanager.conf` | deployment/ | إعدادات Nginx للـ Ubuntu |
| `taskmanager.service` | deployment/systemd/ | خدمة Systemd للتشغيل التلقائي |

---

## ⚖️ مقارنة: Docker مقابل Ubuntu VM

| المعيار | Docker | Ubuntu VM |
|-------|--------|-----------|
| **البدء السريع** | جداً (أمر واحد) | متوسط (خطوات متعددة) |
| **الموارد** | متعددة | أقل |
| **الصيانة** | سهلة | متوسطة |
| **الإنتاج** | نعم (Kubernetes) | نعم (خوادم تقليدية) |

---

## 📞 الدعم والمساهمة

### الإبلاغ عن المشاكل

1. تحقق من [قسم حل المشاكل](#-حل-المشاكل-الشائعة) أولاً
2. فتح **Issue** جديد مع وصف دقيق للمشكلة
3. أرفق السجلات والرسائل الخطأ

### المساهمة في المشروع

1. Fork المشروع
2. إنشاء فرع جديد (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

---

## 📄 الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE) - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

## 👨‍💻 المطور

تم تطوير هذا المشروع بـ ❤️

---

## 📚 موارد إضافية

- [وثائق Flask](https://flask.palletsprojects.com/)
- [وثائق MySQL](https://dev.mysql.com/doc/)
- [وثائق Docker](https://docs.docker.com/)
- [وثائق Nginx](https://nginx.org/en/docs/)

---

**آخر تحديث:** April 2026
**الإصدار:** 1.0.0
# 📋 Task Manager - نظام إدارة المهام

<div align="center">

**نظام إدارة مهام متقدم مبني بـ Flask + MySQL + Python**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](docker-compose.yml)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](#)

[الميزات](#-الميزات) • [الثبت](#-التثبيت) • [الاستخدام](#-الاستخدام) • [النشر](#-النشر)

</div>

---

## 📖 جدول المحتويات

1. [🎯 نظرة عامة](#-نظرة-عامة)
2. [✨ الميزات](#-الميزات)
3. [🛠️ التقنيات المستخدمة](#%EF%B8%8F-التقنيات-المستخدمة)
4. [📁 هيكل المشروع](#-هيكل-المشروع)
5. [🐳 التشغيل بـ Docker](#-التشغيل-بـ-docker)
6. [🖥️ التثبيت على Ubuntu](#%EF%B8%8F-التثبيت-على-ubuntu-vm)
7. [🔧 أوامر الإدارة](#-أوامر-الإدارة)
8. [🌐 بنية النظام](#-بنية-النظام)
9. [🔒 الأمان](#-الأمان)
10. [🐛 حل المشاكل](#-حل-المشاكل-الشائعة)

---

## 🎯 نظرة عامة

**Task Manager** هو نظام متكامل لإدارة المهام والمشاريع يوفر:
- ✅ إدارة المهام بكفاءة
- 📂 تنظيم المهام بفئات
- 👤 نظام المستخدمين (تسجيل دخول/تسجيل)
- 📊 لوحة تحكم شاملة
- 🔐 أمان عالي المستوى

---

## ✨ الميزات

- **واجهة استخدام حديثة**: HTML + CSS + JavaScript
- **قاعدة بيانات قوية**: MySQL مع دعم UTF-8
- **توازن الأحمال**: Nginx كـ Reverse Proxy
- **سهولة النشر**: Docker و Systemd
- **مرن**: يعمل على التطوير والإنتاج
- **آمن**: تشفير كامل والاتصالات المحمية

---

## 🛠️ التقنيات المستخدمة

| الطبقة | التقنية |
|------|---------|
| **الواجهة الأمامية** | HTML5, CSS3, JavaScript |
| **الخادم** | Flask (Python 3.8+) |
| **قاعدة البيانات** | MySQL 8.0 |
| **خادم الويب** | Nginx + Gunicorn |
| **التكامل** | Docker & Docker Compose |
| **النشر** | Systemd & Nginx |

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
#   t a s k - m a n a g e r 
 
 