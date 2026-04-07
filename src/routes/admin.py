from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import User, Produit, LogAcces

admin_bp = Blueprint("admin", __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Acces reserve aux administrateurs.", "danger")
            return redirect(url_for("main.dashboard"))
        return f(*args, **kwargs)
    return login_required(decorated)

@admin_bp.route("/")
@admin_required
def index():
    stats = {"nb_users": User.query.count(), "nb_produits": Produit.query.count(), "nb_logs": LogAcces.query.count()}
    logs  = LogAcces.query.order_by(LogAcces.timestamp.desc()).limit(20).all()
    return render_template("admin/index.html", stats=stats, logs=logs, titre="Back-office")

@admin_bp.route("/users")
@admin_required
def users():
    return render_template("admin/users.html", users=User.query.order_by(User.username).all(), titre="Utilisateurs")

@admin_bp.route("/users/create", methods=["GET","POST"])
@admin_required
def create_user():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        if User.query.filter_by(username=username).first():
            flash(f"'{username}' existe deja.", "danger")
        else:
            u = User(username=username, email=request.form.get("email",""), role=request.form.get("role","viewer"))
            u.set_password(request.form.get("password",""))
            db.session.add(u); db.session.commit()
            flash(f"Utilisateur '{username}' cree.", "success")
            return redirect(url_for("admin.users"))
    return render_template("admin/create_user.html", titre="Creer un utilisateur")

@admin_bp.route("/users/<int:uid>/toggle")
@admin_required
def toggle_user(uid):
    u = User.query.get_or_404(uid)
    if u.id == current_user.id:
        flash("Impossible de desactiver votre propre compte.", "warning")
    else:
        u.actif = not u.actif; db.session.commit()
        flash(f"Compte {'active' if u.actif else 'desactive'}.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/logs")
@admin_required
def logs():
    page     = request.args.get("page", 1, type=int)
    logs_pag = LogAcces.query.order_by(LogAcces.timestamp.desc()).paginate(page=page, per_page=50, error_out=False)
    return render_template("admin/logs.html", logs=logs_pag, titre="Journal des acces")
