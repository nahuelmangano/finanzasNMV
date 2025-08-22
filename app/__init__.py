
import os
from flask import Flask
from .config import Config
from .extensions import db, login_manager, csrf
from .models import User
from .auth.routes import auth_bp
from .expenses.routes import expenses_bp
from .services.routes import services_bp
from .dashboard.routes import dashboard_bp

def _normalize_database_url(url: str) -> str:
    if not url:
        return url
    # Ensure dialect and sslmode=require for Neon
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    if "postgresql+psycopg2://" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg2://")
        if "://" not in url:
            url = "postgresql+psycopg2://" + url.lstrip("/")
    if "sslmode=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return url

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Normalize DB URL for Neon
    app.config["SQLALCHEMY_DATABASE_URI"] = _normalize_database_url(
        app.config.get("SQLALCHEMY_DATABASE_URI", os.getenv("DATABASE_URL", ""))
    )

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        # Create all tables if they don't exist
        db.create_all()

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(expenses_bp, url_prefix="/expenses")
    app.register_blueprint(services_bp, url_prefix="/services")
    app.register_blueprint(dashboard_bp, url_prefix="/")

    # Flask CLI: init-db
    @app.cli.command("init-db")
    def init_db():
        from .models import User, Category, Expense, Service
        db.create_all()
        print("Database initialized.")

    return app
