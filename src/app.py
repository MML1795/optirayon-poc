import os, sys, yaml, logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from dotenv import load_dotenv

SRC_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
for p in [SRC_DIR, ROOT_DIR]:
    if p not in sys.path: sys.path.insert(0, p)
#load_dotenv(os.path.join(ROOT_DIR, ".env"))
# load_dotenv désactivé — on utilise les variables d'environnement système

from extensions import db, login_manager

def create_app(config_path=None):
    if config_path is None:
        config_path = os.path.join(ROOT_DIR, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    app = Flask(__name__,
        template_folder=os.path.join(SRC_DIR, "templates"),
        static_folder=os.path.join(SRC_DIR, "static"))
    data_dir = os.path.join(ROOT_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    db_file    = os.path.join(data_dir, "nondetention.db")
    sqlite_uri = "sqlite:///" + db_file.replace("\\", "/")
    db_uri     = os.environ.get("DATABASE_URL", sqlite_uri)
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)
    print(f"[DB] {db_uri}")
    app.config["SECRET_KEY"]              = os.environ.get("SECRET_KEY", "dev-key-syraliyacom-2025")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"]         = False
    app.config["APP_CONFIG"]              = config
    app.config["ROOT_DIR"]                = ROOT_DIR
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view             = "auth.login"
    login_manager.login_message          = "Veuillez vous connecter."
    login_manager.login_message_category = "warning"
    from routes.auth  import auth_bp
    from routes.main  import main_bp
    from routes.admin import admin_bp
    app.register_blueprint(auth_bp,  url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    os.makedirs(os.path.join(ROOT_DIR, "logs"), exist_ok=True)
    with app.app_context():
        import models  # noqa — enregistre les modèles
        db.create_all()
        print("[DB] Tables OK")
    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return db.session.get(User, int(user_id))

if __name__ == "__main__":
    app = create_app()
    print("\n OK - http://localhost:5000  -  admin / syraliyacom2025!\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
