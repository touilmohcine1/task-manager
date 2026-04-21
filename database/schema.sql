-- ============================================================
-- Task Manager Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE taskmanager;

-- ============================================================
-- Users Table
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(120) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    avatar      VARCHAR(10)  DEFAULT '👤',
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================
-- Categories Table
-- ============================================================
CREATE TABLE IF NOT EXISTS categories (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    color      VARCHAR(7)  DEFAULT '#6366f1',
    icon       VARCHAR(10) DEFAULT '📁',
    user_id    INT         NOT NULL,
    created_at DATETIME    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- Tasks Table
-- ============================================================
CREATE TABLE IF NOT EXISTS tasks (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    description  TEXT,
    status       ENUM('todo', 'in_progress', 'done') DEFAULT 'todo',
    priority     ENUM('low', 'medium', 'high')        DEFAULT 'medium',
    due_date     DATE,
    user_id      INT NOT NULL,
    category_id  INT,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)    REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- ============================================================
-- Seed Data
-- ============================================================
INSERT INTO users (username, email, password, avatar) VALUES
('admin', 'admin@tasks.com', 'pbkdf2:sha256:600000$placeholder$hash', '🧑‍💻');

INSERT INTO categories (name, color, icon, user_id) VALUES
('العمل',       '#6366f1', '💼', 1),
('الشخصية',    '#ec4899', '🏠', 1),
('التعلم',     '#f59e0b', '📚', 1),
('الصحة',      '#10b981', '💪', 1);

INSERT INTO tasks (title, description, status, priority, due_date, user_id, category_id) VALUES
('إعداد تقرير أسبوعي',   'تجميع بيانات الأسبوع وإرسال التقرير للفريق', 'todo',        'high',   CURDATE() + INTERVAL 2 DAY, 1, 1),
('قراءة كتاب Python',    'إنهاء الفصول من 5 إلى 8',                     'in_progress', 'medium', CURDATE() + INTERVAL 7 DAY, 1, 3),
('التمرين اليومي',       '30 دقيقة جري + تمارين إطالة',                 'done',        'high',   CURDATE(),                  1, 4),
('مراجعة الكود',         'مراجعة Pull Requests المعلقة',                'todo',        'medium', CURDATE() + INTERVAL 1 DAY, 1, 1),
('التسوق الأسبوعي',      'شراء مستلزمات المنزل',                        'todo',        'low',    CURDATE() + INTERVAL 3 DAY, 1, 2);
