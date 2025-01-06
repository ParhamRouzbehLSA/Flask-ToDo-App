from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()  # نمونه‌ی واحد از SQLAlchemy
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # مقداردهی db و login_manager
    db.init_app(app)
    login_manager.init_app(app)

    # تنظیم secret_key
    app.config['SECRET_KEY'] = 'your_secret_key'

    # تعریف user_loader
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ثبت Blueprint ها
    from .routes import routes
    app.register_blueprint(routes)

    return app
