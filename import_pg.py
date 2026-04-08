import os, sys
os.environ["DATABASE_URL"] = "postgresql://postgres.yifuxkgywsphkzfmcwel:thesenexa2026@aws-1-eu-central-1.pooler.supabase.com:6543/postgres"
sys.path.insert(0, "src")
import pandas as pd, numpy as np, joblib
from app import create_app
from extensions import db
from models import User, Produit

CSV = r"C:\Users\Utilisateur\Downloads\Détention Market simplifiée - top 500 M2M_DNP - TOP 500 M2M_Tableau (3).csv"
FEATURES = ["Nb jours sans ventes","Stock UG","SMP","VMH mag","VMH nat","CA TTC mag 3 mois"]

df     = pd.read_csv(CSV)
model  = joblib.load("models/model_lasso.pkl")
scaler = joblib.load("models/scaler.pkl")
X      = df[FEATURES].apply(pd.to_numeric, errors="coerce").fillna(0)
df["potentiel_predit"] = np.maximum(model.predict(scaler.transform(X)), 0)

app = create_app()
print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])

with app.app_context():
    db.create_all()
    for username, email, role, pwd in [
        ("admin","admin@syraliyacom.fr","admin","syraliyacom2025!"),
        ("viewer","viewer@syraliyacom.fr","viewer","viewer2025"),
        ("rayon_liquides","rayon@syraliyacom.fr","rayon","liquides2025"),
    ]:
        if not User.query.filter_by(username=username).first():
            u = User(username=username, email=email, role=role)
            u.set_password(pwd)
            db.session.add(u)
            print(f"User cree: {username}")
    db.session.commit()
    Produit.query.delete()
    db.session.commit()
    for _, row in df.iterrows():
        def g(c):
            v = row.get(c)
            try: return float(v) if pd.notna(v) else None
            except: return None
        db.session.add(Produit(
            barcode=g("Barcode"),
            rayon=str(row.get("Rayon","")) if pd.notna(row.get("Rayon")) else None,
            famille=str(row.get("Famille","")) if pd.notna(row.get("Famille")) else None,
            libelle=str(row.get("Produit","")) if pd.notna(row.get("Produit")) else None,
            nb_jours_sans_ventes=g("Nb jours sans ventes"),
            stock_ug=g("Stock UG"), smp=g("SMP"),
            vmh_mag=g("VMH mag"), vmh_nat=g("VMH nat"),
            ca_ttc_mag_3mois=g("CA TTC mag 3 mois"),
            potentiel_gain_mensuel=g("Potentiel gain mensuel"),
            potentiel_predit=g("potentiel_predit")
        ))
    db.session.commit()
    print("Import termine :", Produit.query.count(), "produits!")