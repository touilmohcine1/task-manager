"""
Task Manager — Entry Point
Run:  python run.py              (dev)
      gunicorn run:app           (prod)
"""
from app import create_app, db

app = create_app()

if __name__ == "__main__":
    import os
    with app.app_context():
        db.create_all()
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
