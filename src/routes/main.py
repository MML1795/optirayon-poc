import io, csv
from datetime import datetime
from flask import Blueprint, render_template, request, make_response, current_app, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc, asc
from extensions import db
from models import Produit, LogAcces, Commentaire, HistoriqueAction

main_bp = Blueprint("main", __name__)

def _log(action, detail=None):
    db.session.add(LogAcces(
        user_id=current_user.id if current_user.is_authenticated else None,
        username=current_user.username if current_user.is_authenticated else "anonyme",
        action=action, detail=detail, ip_address=request.remote_addr))
    db.session.commit()

@main_bp.route("/")
@login_required
def dashboard():
    cfg   = current_app.config["APP_CONFIG"]
    top   = Produit.query.filter(Produit.potentiel_predit.isnot(None))\
              .order_by(desc(Produit.potentiel_predit)).limit(cfg["ui"]["top_produits_dashboard"]).all()
    tous  = Produit.query.filter(Produit.potentiel_predit.isnot(None)).all()
    vals  = [p.potentiel_predit for p in tous if p.potentiel_predit]
    stats = {
        "nb_produits":       len(tous),
        "gain_total":        round(sum(vals), 0) if vals else 0,
        "gain_moyen":        round(sum(vals)/len(vals), 0) if vals else 0,
        "nb_haute_priorite": sum(1 for v in vals if v >= cfg["ui"]["seuil_priorite_haute"]),
    }
    rayons_data = db.session.query(
        Produit.rayon,
        db.func.count(Produit.id).label("nb"),
        db.func.sum(Produit.potentiel_predit).label("gain_total"),
    ).group_by(Produit.rayon).all()
    statuts_data = db.session.query(
        Produit.statut,
        db.func.count(Produit.id).label("nb")
    ).group_by(Produit.statut).all()
    top_familles = db.session.query(
        Produit.famille,
        db.func.sum(Produit.potentiel_predit).label("gain_total")
    ).group_by(Produit.famille)\
     .order_by(desc("gain_total")).limit(5).all()
    _log("dashboard")
    return render_template("dashboard.html",
        top_produits=top, stats=stats,
        rayons=rayons_data, statuts_data=statuts_data,
        top_familles=top_familles, titre="Tableau de bord")

@main_bp.route("/api/familles")
@login_required
def api_familles():
    rayon = request.args.get("rayon", "")
    q = db.session.query(Produit.famille).filter(Produit.famille.isnot(None))
    if rayon:
        q = q.filter(Produit.rayon == rayon)
    familles = sorted(set([f[0] for f in q.distinct().all() if f[0]]))
    return jsonify(familles)

@main_bp.route("/liste")
@login_required
def liste():
    cfg    = current_app.config["APP_CONFIG"]
    rayon  = request.args.get("rayon", "")
    fam    = request.args.get("famille", "")
    seuil  = request.args.get("seuil", "")
    tri    = request.args.get("tri", "predit_desc")
    page   = request.args.get("page", 1, type=int)
    statut = request.args.get("statut", "")
    search = request.args.get("search", "").strip()
    q = Produit.query.filter(Produit.potentiel_predit.isnot(None))
    if rayon:  q = q.filter(Produit.rayon == rayon)
    if fam:    q = q.filter(Produit.famille == fam)
    if statut: q = q.filter(Produit.statut == statut)
    if seuil:
        try: q = q.filter(Produit.potentiel_predit >= float(seuil))
        except: pass
    if search:
        q = q.filter(
            db.or_(
                Produit.libelle.ilike(f"%{search}%"),
                db.cast(Produit.barcode, db.String).ilike(f"%{search}%")
            )
        )
    ordre = {
        "predit_desc":  desc(Produit.potentiel_predit),
        "predit_asc":   asc(Produit.potentiel_predit),
        "jours_desc":   desc(Produit.nb_jours_sans_ventes),
        "famille_asc":  asc(Produit.famille),
        "libelle_asc":  asc(Produit.libelle),
    }
    pag = q.order_by(ordre.get(tri, desc(Produit.potentiel_predit)))\
           .paginate(page=page, per_page=cfg["ui"]["items_per_page"], error_out=False)
    rayons_dispo   = sorted(set([r[0] for r in db.session.query(Produit.rayon).distinct().all() if r[0]]))
    fq = db.session.query(Produit.famille)
    if rayon: fq = fq.filter(Produit.rayon == rayon)
    familles_dispo = sorted(set([f[0] for f in fq.distinct().all() if f[0]]))
    return render_template("liste.html", produits=pag.items, pagination=pag,
        rayons=rayons_dispo, familles=familles_dispo,
        rayon_filtre=rayon, famille_filtre=fam, seuil_filtre=seuil,
        statut_filtre=statut, search=search, tri=tri,
        titre="Liste des produits non détenus")

@main_bp.route("/produit/<int:pid>")
@login_required
def detail_produit(pid):
    p = Produit.query.get_or_404(pid)
    commentaires = Commentaire.query.filter_by(produit_id=pid).order_by(desc(Commentaire.timestamp)).all()
    historique   = HistoriqueAction.query.filter_by(produit_id=pid).order_by(desc(HistoriqueAction.timestamp)).all()
    _log("detail_produit", f"#{pid}")
    return render_template("detail.html", produit=p, commentaires=commentaires,
                           historique=historique, titre="Fiche produit")

@main_bp.route("/produit/<int:pid>/statut", methods=["POST"])
@login_required
def update_statut(pid):
    p = Produit.query.get_or_404(pid)
    ancien_statut = p.statut
    nouveau_statut = request.form.get("statut")
    if nouveau_statut in ["a_traiter", "en_cours", "traite"]:
        p.statut = nouveau_statut
        db.session.add(HistoriqueAction(
            produit_id=pid, user_id=current_user.id,
            username=current_user.username, action="changement_statut",
            detail=f"{ancien_statut} → {nouveau_statut}"
        ))
        db.session.commit()
        flash(f"Statut mis à jour : {p.statut_label()}", "success")
    return redirect(url_for("main.detail_produit", pid=pid))

@main_bp.route("/produit/<int:pid>/commentaire", methods=["POST"])
@login_required
def add_commentaire(pid):
    contenu = request.form.get("contenu", "").strip()
    if contenu:
        db.session.add(Commentaire(
            produit_id=pid, user_id=current_user.id,
            username=current_user.username, contenu=contenu
        ))
        db.session.add(HistoriqueAction(
            produit_id=pid, user_id=current_user.id,
            username=current_user.username, action="commentaire",
            detail=contenu[:100]
        ))
        db.session.commit()
        flash("Commentaire ajouté.", "success")
    return redirect(url_for("main.detail_produit", pid=pid))

@main_bp.route("/export")
@login_required
def export_csv():
    cfg = current_app.config["APP_CONFIG"]
    produits = Produit.query.filter(Produit.potentiel_predit.isnot(None))\
        .order_by(desc(Produit.potentiel_predit)).limit(cfg["export"]["max_rows"]).all()
    output = io.StringIO()
    w = csv.writer(output, delimiter=";")
    w.writerow(["Rang","Barcode","Libelle","Rayon","Famille","Potentiel predit (EUR)",
                "Jours sans vente","Statut","Priorite","Date export"])
    for i, p in enumerate(produits, 1):
        w.writerow([i, p.barcode, p.libelle or "", p.rayon, p.famille,
            f"{p.potentiel_predit:.2f}" if p.potentiel_predit else "",
            p.nb_jours_sans_ventes or "", p.statut_label(), p.priorite(),
            datetime.now().strftime("%Y-%m-%d %H:%M")])
    output.seek(0)
    resp = make_response(output.getvalue())
    resp.headers["Content-Disposition"] = f"attachment; filename=optirayon_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    resp.headers["Content-Type"] = "text/csv; charset=utf-8-sig"
    _log("export_csv", f"{len(produits)} produits")
    return resp