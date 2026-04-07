import os, sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR  = os.path.join(ROOT_DIR, "src")
for p in [SRC_DIR, ROOT_DIR]:
    if p not in sys.path: sys.path.insert(0, p)
from app import create_app
from extensions import db
from models import User

app = create_app()
with app.app_context():
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
            print(f"  Cree : {username}")
        else:
            print(f"  Existe : {username}")
    db.session.commit()
print("\nTermine ! Lancez : python src/app.py")
print("Login : admin / syraliyacom2025!")
