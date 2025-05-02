# opre_be/__init__.py
from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from .config import DB_URL
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})

    # app.config.from_mapping(
    #     DB_URL=DB_URL,
    #     JWT_SECRET_KEY="your-super-secret-key"
    # )

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)

    app.database = create_engine(app.config['DB_URL'], max_overflow=0, echo=True)

    JWTManager(app)

    # ✅ blueprint 등록
    from .routes.auth import auth_bp
    from .routes.recipes import recipe_bp
    from .routes.t_endpoints import test_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(recipe_bp)

    return app

