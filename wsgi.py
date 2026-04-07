import os, sys
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from app import create_app
from extensions import db

app = create_app()

# Création automatique des users au démarrage
with app.app_context():
    from models import User
    db.create_all()
    for username, email, role, pwd in [
        ("admin",          "admin@syraliyacom.fr",  "admin",  "syraliyacom2025!"),
        ("viewer",         "viewer@syraliyacom.fr", "viewer", "viewer2025"),
        ("rayon_liquides", "rayon@syraliyacom.fr",  "rayon",  "liquides2025"),
    ]:
        if not User.query.filter_by(username=username).first():
            u = User(username=username, email=email, role=role)
            u.set_password(pwd)
            db.session.add(u)
            print(f"User cree: {username}")
    db.session.commit()

if __name__ == "__main__":
    app.run()