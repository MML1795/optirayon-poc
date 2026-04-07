from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, LogAcces

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username, actif=True).first()
        if user and user.check_password(password):
            login_user(user)
            user.derniere_connexion = datetime.utcnow()
            db.session.add(LogAcces(username=username, action="login_success", ip_address=request.remote_addr))
            db.session.commit()
            return redirect(request.args.get("next") or url_for("main.dashboard"))
        db.session.add(LogAcces(username=username, action="login_failure", ip_address=request.remote_addr))
        db.session.commit()
        flash("Identifiant ou mot de passe incorrect.", "danger")
    return render_template("login.html", titre="Connexion")

@auth_bp.route("/logout")
@login_required
def logout():
    db.session.add(LogAcces(username=current_user.username, action="logout", ip_address=request.remote_addr))
    db.session.commit()
    logout_user()
    flash("Vous avez ete deconnecte.", "info")
    return redirect(url_for("auth.login"))
