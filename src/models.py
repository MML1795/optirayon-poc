from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id                 = db.Column(db.Integer, primary_key=True)
    username           = db.Column(db.String(64),  unique=True, nullable=False)
    email              = db.Column(db.String(128), unique=True, nullable=False)
    password_hash      = db.Column(db.String(256), nullable=False)
    role               = db.Column(db.String(32),  nullable=False, default="viewer")
    actif              = db.Column(db.Boolean, default=True)
    date_creation      = db.Column(db.DateTime, default=datetime.utcnow)
    derniere_connexion = db.Column(db.DateTime, nullable=True)
    def set_password(self, pwd): self.password_hash = generate_password_hash(pwd)
    def check_password(self, pwd): return check_password_hash(self.password_hash, pwd)
    def is_admin(self): return self.role == "admin"

class Produit(db.Model):
    __tablename__ = "produits"
    id                     = db.Column(db.Integer, primary_key=True)
    barcode                = db.Column(db.BigInteger, nullable=True)
    rayon                  = db.Column(db.String(64),  nullable=True)
    famille                = db.Column(db.String(128), nullable=True)
    libelle                = db.Column(db.String(256), nullable=True)
    nb_jours_sans_ventes   = db.Column(db.Float, nullable=True)
    stock_ug               = db.Column(db.Float, nullable=True)
    smp                    = db.Column(db.Float, nullable=True)
    vmh_mag                = db.Column(db.Float, nullable=True)
    vmh_nat                = db.Column(db.Float, nullable=True)
    ca_ttc_mag_3mois       = db.Column(db.Float, nullable=True)
    potentiel_gain_mensuel = db.Column(db.Float, nullable=True)
    potentiel_predit       = db.Column(db.Float, nullable=True)
    date_import            = db.Column(db.DateTime, default=datetime.utcnow)
    statut                 = db.Column(db.String(32), nullable=False, default="a_traiter")
    commentaires           = db.relationship("Commentaire", backref="produit", lazy="dynamic", cascade="all, delete-orphan")
    historique             = db.relationship("HistoriqueAction", backref="produit", lazy="dynamic", cascade="all, delete-orphan")

    def priorite(self):
        v = self.potentiel_predit or 0
        if v >= 500: return "haute"
        if v >= 200: return "moyenne"
        return "basse"

    def statut_label(self):
        return {"a_traiter": "À traiter", "en_cours": "En cours", "traite": "Traité"}.get(self.statut, "À traiter")

    def statut_color(self):
        return {"a_traiter": "rouge", "en_cours": "orange", "traite": "vert"}.get(self.statut, "rouge")

class Commentaire(db.Model):
    __tablename__ = "commentaires"
    id         = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey("produits.id"), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    username   = db.Column(db.String(64), nullable=True)
    contenu    = db.Column(db.Text, nullable=False)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

class HistoriqueAction(db.Model):
    __tablename__ = "historique_actions"
    id         = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey("produits.id"), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    username   = db.Column(db.String(64), nullable=True)
    action     = db.Column(db.String(128), nullable=False)
    detail     = db.Column(db.String(512), nullable=True)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

class LogAcces(db.Model):
    __tablename__ = "logs_acces"
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    username   = db.Column(db.String(64),  nullable=True)
    action     = db.Column(db.String(128), nullable=False)
    detail     = db.Column(db.String(512), nullable=True)
    ip_address = db.Column(db.String(45),  nullable=True)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)