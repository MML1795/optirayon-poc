# Non-Détention Produit — Application d'aide à la décision
**Proof of Concept — Mémoire de fin d'études Master 2 Data & IA**
**Auteure : Marielle Ladhari — SARL SYRALIYACOM Distribution / Carrefour Express**
**Année universitaire : 2025–2026**

---

## 📋 Description du projet

Cette application web Flask permet de prioriser les décisions opérationnelles liées à la
non-détention produit dans un point de vente Carrefour Express. Elle s'appuie sur un modèle
de machine learning supervisé (régression Lasso) pour estimer le potentiel de gain mensuel
de chaque produit non détenu, et présente les résultats sous forme de tableau interactif
classé par ordre de priorité décroissante.

**URL publique (POC local) :** http://syraliyacom-nondetention.local:5000
**Dépôt Git :** https://github.com/mladhari/nondetention-poc

---

## ⚙️ Prérequis

| Outil | Version minimale |
|-------|-----------------|
| Python | 3.10+ |
| pip | 22.0+ |
| SQLite | 3.39+ (inclus Python) |
| Navigateur | Chrome 110+, Firefox 110+, Edge 110+, Safari 16+ |
| OS | Windows 10/11, macOS 12+, Ubuntu 20.04+ |

> **Note :** Aucune connexion internet n'est requise après installation.
> Tous les assets (CSS, JS) sont servis localement.

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/mladhari/nondetention-poc.git
cd nondetention-poc
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
# Éditer .env avec vos valeurs (voir section ci-dessous)
```

### 5. Initialiser la base de données

```bash
python scripts/init_db.py
```

Ce script :
- Crée la base SQLite `data/nondetention.db`
- Importe les données depuis le CSV source
- Crée les index nécessaires aux performances

### 6. Lancer l'application

```bash
python src/app.py
```

L'application est accessible à l'adresse : **http://localhost:5000**

---

## 🔐 Identifiants de test

| Rôle | Identifiant | Mot de passe |
|------|-------------|--------------|
| Administrateur | `admin` | `syraliyacom2025!` |
| Consultation | `viewer` | `viewer2025` |
| Chef de rayon | `rayon_liquides` | `liquides2025` |

> ⚠️ Ces identifiants sont à usage de test uniquement.
> En production, modifier impérativement les mots de passe dans `.env`.

---

## 🗄️ Connexion à la base de données SQL

### Base SQLite (développement / POC)

```python
# Connexion automatique via SQLAlchemy (configurée dans config.yaml)
DATABASE_URL = "sqlite:///data/nondetention.db"
```

### Import du dump SQL

```bash
# Restaurer la base depuis le dump fourni
sqlite3 data/nondetention.db < nondetention_dump.sql
```

### Accès direct à la base

```bash
sqlite3 data/nondetention.db
# Dans SQLite :
.tables          # Lister les tables
.schema produits # Schéma de la table produits
SELECT COUNT(*) FROM produits;
```

### Tables principales

| Table | Description | Nb lignes (POC) |
|-------|-------------|-----------------|
| `produits` | Catalogue produits non détenus | ~8 500 |
| `predictions` | Prédictions du modèle Lasso | ~8 500 |
| `rayons` | Référentiel rayons/familles | 3 |
| `familles` | Référentiel familles produits | ~87 |
| `users` | Utilisateurs de l'application | 3 |
| `logs_acces` | Journal des connexions | variable |

---

## 🔧 Accès administrateur au back-office

**URL back-office :** http://localhost:5000/admin

**Identifiants admin :** `admin` / `syraliyacom2025!`

### Fonctionnalités back-office

- **Gestion des données :** import d'un nouveau fichier CSV, rafraîchissement des prédictions
- **Gestion des utilisateurs :** création, modification, désactivation des comptes
- **Journaux :** consultation des logs d'accès et d'utilisation
- **Modèle IA :** visualisation des métriques du modèle (R², RMSE, MAE), rechargement du modèle
- **Export :** export des recommandations en CSV, des logs en Excel

### Rechargement du modèle Lasso

```bash
# Depuis le back-office > Modèle IA > Recharger
# Ou en ligne de commande :
python scripts/retrain_model.py --input data/nondetention_clean.csv
```

---

## 🌐 Compatibilité multi-navigateur

| Navigateur | Version testée | Statut |
|-----------|---------------|--------|
| Google Chrome | 120+ | ✅ Validé |
| Mozilla Firefox | 119+ | ✅ Validé |
| Microsoft Edge | 120+ | ✅ Validé |
| Safari (macOS) | 17+ | ✅ Validé |
| Safari (iOS) | 17+ | ✅ Validé |
| Chrome (Android) | 120+ | ✅ Validé |

---

## 📁 Structure du projet

```
nondetention_poc/
├── src/
│   ├── app.py              # Point d'entrée Flask
│   ├── routes/
│   │   ├── main.py         # Routes principales (dashboard, liste)
│   │   ├── auth.py         # Authentification (login/logout)
│   │   └── admin.py        # Routes back-office
│   ├── models/
│   │   ├── prediction.py   # Logique de prédiction Lasso
│   │   └── database.py     # Modèles SQLAlchemy
│   ├── templates/
│   │   ├── base.html       # Template de base
│   │   ├── dashboard.html  # Tableau de bord
│   │   ├── liste.html      # Liste des produits
│   │   ├── detail.html     # Fiche produit
│   │   ├── login.html      # Page de connexion
│   │   └── admin/          # Templates back-office
│   └── static/
│       ├── css/style.css   # Styles de l'application
│       └── js/main.js      # Scripts frontend
├── models/
│   ├── model_lasso.pkl     # Modèle Lasso sérialisé
│   └── scaler.pkl          # StandardScaler ajusté
├── data/
│   └── nondetention.db     # Base SQLite (générée)
├── scripts/
│   ├── init_db.py          # Initialisation base de données
│   └── retrain_model.py    # Réentraînement du modèle
├── nondetention_dump.sql   # Dump SQL de la base
├── config.yaml             # Configuration application
├── requirements.txt        # Dépendances Python
├── .env.example            # Template variables d'environnement
└── README.md               # Ce fichier
```

---

## 🛡️ Sécurité et RGPD

- Aucune donnée personnelle identifiable dans le jeu de données
- Authentification par session Flask sécurisée (SECRET_KEY configurée dans `.env`)
- Journalisation des accès avec horodatage
- Accès restreint par rôle (admin / viewer / chef de rayon)
- Séparation stricte des environnements test et production

---

## 📞 Contact

**Auteure :** Marielle Ladhari — marielle.ladhari@nexa.fr
**Tuteur entreprise :** Direction SARL SYRALIYACOM Distribution
**Établissement :** Nexa Digital School — Master 2 Data & IA (RNCP 37137)
