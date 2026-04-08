import os, sys
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    from models import User, Produit
    db.create_all()
    if User.query.count() == 0:
        for username, email, role, pwd in [
            ("admin", "admin@syraliyacom.fr", "admin", "syraliyacom2025!"),
            ("viewer", "viewer@syraliyacom.fr", "viewer", "viewer2025"),
            ("rayon_liquides", "rayon@syraliyacom.fr", "rayon", "liquides2025"),
        ]:
            u = User(username=username, email=email, role=role)
            u.set_password(pwd)
            db.session.add(u)
        db.session.commit()
        print("Users créés")

if __name__ == "__main__":
    app.run()