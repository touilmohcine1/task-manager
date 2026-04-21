#!/bin/bash
# ============================================================
#  Task Manager — Ubuntu VM Installer
#  Run as root:  sudo bash install.sh
# ============================================================
set -e   # exit on any error

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; NC='\033[0m'

info()  { echo -e "${CYAN}[INFO]${NC}  $1"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ── Must be root ────────────────────────────────────────────
[[ $EUID -ne 0 ]] && error "Run this script as root: sudo bash install.sh"

# ── Variables ───────────────────────────────────────────────
APP_DIR="/opt/taskmanager"
APP_USER="taskmanager"
DB_NAME="taskmanager"
DB_USER="taskuser"
DB_PASS="StrongPass123!"          # ← Change before running!
SECRET_KEY="$(openssl rand -hex 24)"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║      Task Manager — Ubuntu Installer     ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── 1. System Update ────────────────────────────────────────
info "Updating system packages..."
apt-get update -qq && apt-get upgrade -y -qq
ok "System updated"

# ── 2. Install Dependencies ─────────────────────────────────
info "Installing Python 3, MySQL, Nginx, Git..."
apt-get install -y -qq \
    python3 python3-pip python3-venv \
    mysql-server \
    nginx \
    git \
    curl \
    pkg-config \
    libmysqlclient-dev \
    build-essential
ok "Dependencies installed"

# ── 3. Create App User ──────────────────────────────────────
info "Creating system user: $APP_USER"
if ! id "$APP_USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$APP_DIR" "$APP_USER"
    ok "User $APP_USER created"
else
    warn "User $APP_USER already exists"
fi

# ── 4. Copy Project Files ───────────────────────────────────
info "Deploying application to $APP_DIR..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [[ -d "$APP_DIR" ]]; then
    warn "$APP_DIR exists — backing up to ${APP_DIR}.bak"
    mv "$APP_DIR" "${APP_DIR}.bak.$(date +%s)"
fi

cp -r "$PROJECT_ROOT" "$APP_DIR"
ok "Files copied to $APP_DIR"

# ── 5. Python Virtual Environment ───────────────────────────
info "Creating Python virtual environment..."
python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip -q
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt" -q
ok "Virtual environment ready"

# ── 6. Configure MySQL ──────────────────────────────────────
info "Configuring MySQL..."
systemctl enable mysql --now

# Secure and configure
mysql -u root <<SQL
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
SQL

# Load schema
mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < "$APP_DIR/database/schema.sql"
ok "MySQL configured and schema loaded"

# ── 7. Create .env File ─────────────────────────────────────
info "Writing .env file..."
cat > "$APP_DIR/backend/.env" <<ENV
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=${SECRET_KEY}

DB_HOST=localhost
DB_PORT=3306
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASS}

APP_HOST=127.0.0.1
APP_PORT=5000
ENV
ok ".env created"

# ── 8. Initialize Flask DB ──────────────────────────────────
info "Initializing Flask database..."
cd "$APP_DIR/backend"
"$APP_DIR/venv/bin/python" -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Tables created OK')
"
ok "Flask database initialized"

# ── 9. Log Directory ────────────────────────────────────────
info "Creating log directory..."
mkdir -p /var/log/taskmanager
chown "$APP_USER":"$APP_USER" /var/log/taskmanager
ok "Log directory ready"

# ── 10. Set Permissions ─────────────────────────────────────
info "Setting file permissions..."
chown -R "$APP_USER":"$APP_USER" "$APP_DIR"
chmod 640 "$APP_DIR/backend/.env"
ok "Permissions set"

# ── 11. Systemd Service ─────────────────────────────────────
info "Installing systemd service..."
cp "$APP_DIR/deployment/systemd/taskmanager.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable taskmanager    # ← Starts automatically on boot
systemctl start  taskmanager
ok "Systemd service enabled and started"

# ── 12. Nginx Config ────────────────────────────────────────
info "Configuring Nginx..."
cp "$APP_DIR/deployment/nginx-taskmanager.conf" /etc/nginx/sites-available/taskmanager
ln -sf /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled/taskmanager
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
ok "Nginx configured"

# ── 13. Firewall ────────────────────────────────────────────
info "Configuring UFW firewall..."
ufw allow OpenSSH  -q
ufw allow 'Nginx Full' -q
ufw --force enable
ok "Firewall configured"

# ── Done ────────────────────────────────────────────────────
SERVER_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║        Installation Complete! ✅          ║"
echo "╠══════════════════════════════════════════╣"
echo "║  App URL:  http://${SERVER_IP}           "
echo "║  Logs:     journalctl -u taskmanager -f  "
echo "║  Status:   systemctl status taskmanager  "
echo "╚══════════════════════════════════════════╝"
echo ""
