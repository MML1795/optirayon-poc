# OptiRayon — Application d'aide à la décision
**Proof of Concept — Mémoire de fin d'études Master 2 Data & IA**
**Auteure : Marielle Ladhari — SARL SYRALIYACOM Distribution / Carrefour Express**
**Année universitaire : 2025–2026**

---

## 📋 Description du projet

OptiRayon est une application web Flask permettant de prioriser les décisions opérationnelles
liées à la non-détention produit dans un point de vente Carrefour Express. Elle s'appuie sur un
modèle de machine learning supervisé (régression Lasso, α=0.5) pour estimer le potentiel de gain
mensuel de chaque produit non détenu, et présente les résultats sous forme de tableau interactif
classé par ordre de priorité décroissante.

**🌐 URL publique :** https://optirayon-poc.onrender.com
**📁 Dépôt Git :** https://github.com/MML1795/optirayon-poc

### Identifiants d'accès (évaluateur)

| Rôle | Identifiant | Mot de passe |
|------|-------------|--------------|
| Administrateur | `admin` | `syraliyacom2025!` |
| Consultation | `viewer` | `viewer2025` |
| Chef de rayon | `rayon_liquides` | `liquides2025` |

> ⚠️ L'application est hébergée sur Render (plan gratuit). Si la page met quelques secondes
> à s'afficher, patientez 30 secondes et rafraîchissez — c'est le délai de démarrage normal.

---

## ✨ Fonctionnalités

- 📊 **Tableau de bord** avec 4 indicateurs clés et 3 graphiques interactifs (Chart.js)
- 🔍 **Recherche full-text** par libellé produit ou code-barres
- 🔗 **Filtres dynamiques** : sélectionner un rayon met à jour automatiquement les familles
- 🎯 **Système de statut** : À traiter / En cours / Traité par produit
- 💬 **Commentaires** : annotation de chaque fiche produit
- 📅 **Historique** : traçabilité complète des actions par produit
- ⬇️ **Export CSV** enrichi (libellés, statuts, priorités)
- 👤 **Back-office** : gestion des utilisateurs, des rôles et des journaux d'accès
- 📱 **Design responsive** : compatible desktop et mobile

---

## 📊 Données et modèle

| Indicateur | Valeur |
|-----------|--------|
| Produits analysés | 7 669 |
| Potentiel total récupérable | 3 959 968 € |
| Gain moyen prédit | 517 € / produit |
| Modèle retenu | Lasso (α=0.5) |
| R² test | 0.353 |
| RMSE | 198.8 € |
| MAE | 133.6 € |

---

## ⚙️ Prérequis (installation locale)

| Outil | Version minimale |
|-------|-----------------|
| Python | 3.10+ |
| pip | 22.0+ |
| Navigateur | Chrome 110+, Firefox 110+, Edge 110+, Safari 16+ |
| OS | Windows 10/11, macOS 12+, Ubuntu 20.04+ |

---

## 🚀 Installation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/MML1795/optirayon-poc.git
cd optirayon-poc
```

### 2. Créer et activer l'environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec vos valeurs
```

### 5. Initialiser la base de données

```bash
python scripts/init_db.py
```

### 6. Lancer l'application

```bash
python src/app.py
```

L'application est accessible à l'adresse : **http://localhost:5000**

---

## 🗄️ Base de données

L'application utilise **PostgreSQL hébergé sur Supabase** (cloud, gratuit) en production,
et **SQLite** en développement local.

### Tables principales

| Table | Description | Nb lignes |
|-------|-------------|-----------|
| `produits` | Catalogue produits non détenus avec prédictions | 7 669 |
| `commentaires` | Commentaires par produit | variable |
| `historique_actions` | Historique des changements de statut | variable |
| `users` | Utilisateurs de l'application | 3 |
| `logs_acces` | Journal des connexions et actions | variable |

---

## 🔧 Back-office administrateur

**URL :** https://optirayon-poc.onrender.com/admin
**Identifiants :** `admin` / `syraliyacom2025!`

### Fonctionnalités
- Gestion des utilisateurs (création, activation/désactivation)
- Consultation du journal complet des accès
- Statistiques globales (nb produits, utilisateurs, actions)

---

## 🌐 Compatibilité multi-navigateur

| Navigateur | Statut |
|-----------|--------|
| Google Chrome 120+ | ✅ Validé |
| Mozilla Firefox 119+ | ✅ Validé |
| Microsoft Edge 120+ | ✅ Validé |
| Safari macOS 17+ | ✅ Validé |
| Safari iOS 17+ | ✅ Validé |
| Chrome Android 120+ | ✅ Validé |

---

## 📁 Structure du projet

```
poc_v2/
├── src/
│   ├── app.py              # Point d'entrée Flask
│   ├── extensions.py       # Instance unique db + login_manager
│   ├── models.py           # Modèles SQLAlchemy (User, Produit, Commentaire...)
│   ├── routes/
│   │   ├── main.py         # Dashboard, liste, fiche produit, export CSV
│   │   ├── auth.py         # Authentification (login/logout)
│   │   └── admin.py        # Routes back-office
│   ├── templates/
│   │   ├── base.html       # Template de base
│   │   ├── dashboard.html  # Tableau de bord + graphiques Chart.js
│   │   ├── liste.html      # Liste produits + recherche + filtres
│   │   ├── detail.html     # Fiche produit + statut + commentaires
│   │   ├── login.html      # Page de connexion
│   │   └── admin/          # Templates back-office
│   └── static/
│       ├── css/style.css   # Styles responsive (WCAG 2.1 AA)
│       └── js/main.js      # Scripts frontend
├── models/
│   ├── model_lasso.pkl     # Modèle Lasso sérialisé (α=0.5)
│   └── scaler.pkl          # StandardScaler ajusté
├── scripts/
│   ├── init_db.py          # Initialisation BDD + création utilisateurs
│   └── retrain_model.py    # Réentraînement du modèle Lasso
├── import_pg.py            # Import des données vers PostgreSQL
├── wsgi.py                 # Point d'entrée Render (gunicorn)
├── nondetention_dump.sql   # Dump SQL de la base
├── config.yaml             # Configuration application
├── requirements.txt        # Dépendances Python
├── .env.example            # Template variables d'environnement
└── README.md               # Ce fichier
```

---

## 🚀 Déploiement (Render + Supabase)

| Service | Usage | Plan |
|---------|-------|------|
| Render | Hébergement application Flask | Gratuit |
| Supabase | Base de données PostgreSQL | Gratuit (90 jours) |

**Variables d'environnement Render :**
- `DATABASE_URL` : URL de connexion Supabase PostgreSQL
- `SECRET_KEY` : Clé secrète Flask
- `PYTHON_VERSION` : 3.11.0

---

## 🛡️ Sécurité et RGPD

- Aucune donnée personnelle identifiable dans le jeu de données
- Authentification par session Flask sécurisée
- Journalisation des accès avec horodatage
- Accès restreint par rôle (admin / viewer / rayon)
- Mots de passe hachés avec bcrypt

---

## 📞 Contact

**Auteure :** Marielle Ladhari
**Établissement :** Nexa Digital School — Master 2 Data & IA (RNCP 37137)
**Entreprise :** SARL SYRALIYACOM Distribution — Carrefour Express, Paris 6e
