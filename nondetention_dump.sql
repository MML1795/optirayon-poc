-- ═══════════════════════════════════════════════════════════════════════════
-- nondetention_dump.sql — Export SQL de la base de données
-- Non-Détention Produit — SARL SYRALIYACOM Distribution / Carrefour Express
-- Mémoire Marielle Ladhari — Master 2 Data & IA (RNCP 37137)
-- Date d'export : 2026-04-01
-- Base : SQLite 3.39 (développement / POC)
-- ═══════════════════════════════════════════════════════════════════════════

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

-- ─── Table users ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'viewer',
    actif BOOLEAN DEFAULT 1,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    derniere_connexion DATETIME
);

-- Utilisateurs de test (mots de passe hachés avec bcrypt)
-- Mot de passe réel : voir .env ou README.md
INSERT INTO users (username, email, password_hash, role, actif) VALUES
  ('admin',          'admin@syraliyacom.fr',  '$2b$12$placeholder_admin_hash_bcrypt',  'admin',  1),
  ('viewer',         'viewer@syraliyacom.fr', '$2b$12$placeholder_viewer_hash_bcrypt', 'viewer', 1),
  ('rayon_liquides', 'rayon@syraliyacom.fr',  '$2b$12$placeholder_rayon_hash_bcrypt',  'rayon',  1);

-- ─── Table produits ───────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS produits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode BIGINT,
    rayon VARCHAR(64),
    famille VARCHAR(128),
    sous_famille VARCHAR(128),
    libelle VARCHAR(256),
    nb_jours_sans_ventes REAL,
    stock_ug REAL,
    smp REAL,
    vmh_mag REAL,
    vmh_nat REAL,
    ca_ttc_mag_3mois REAL,
    potentiel_gain_mensuel REAL,
    potentiel_predit REAL,
    date_import DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_produits_rayon ON produits(rayon);
CREATE INDEX IF NOT EXISTS idx_produits_famille ON produits(famille);
CREATE INDEX IF NOT EXISTS idx_produits_barcode ON produits(barcode);
CREATE INDEX IF NOT EXISTS idx_produits_predit ON produits(potentiel_predit DESC);

-- Données de démonstration (extrait anonymisé — 10 produits représentatifs)
INSERT INTO produits (barcode, rayon, famille, nb_jours_sans_ventes, stock_ug, smp, vmh_mag, vmh_nat, ca_ttc_mag_3mois, potentiel_gain_mensuel, potentiel_predit) VALUES
  (3057640257773, '02 - LIQUIDES',  '245 - SODAS,BOISS.FRUITS&JUS FRUITS', 12, 0.0, 75.5, 18.2, 42.1, 1250.0, 667.3, 589.1),
  (3057640112345, '02 - LIQUIDES',  '240 - BIERES ET CIDRES',               5, 2.0, 62.3, 22.4, 38.7, 980.0,  450.2, 412.8),
  (3057640223456, '02 - LIQUIDES',  '200 - VIN AVEC/SANS INDICATION GEOGR', 28, 0.0, 45.8, 8.1,  19.3, 420.0,  312.5, 287.4),
  (3057640334567, '01 - EPICERIE',  '015 - CAFES TORREFIES',                7, 1.0, 52.1, 12.3, 28.4, 680.0,  245.8, 231.6),
  (3057640445678, '03 - D.P.H.',    '300 - HYGIENE',                        3, 5.0, 38.4, 9.7,  22.1, 520.0,  198.4, 185.2),
  (3057640556789, '01 - EPICERIE',  '070 - CHIPS',                          45, 0.0, 28.7, 5.2,  14.8, 230.0,  142.1, 134.7),
  (3057640667890, '02 - LIQUIDES',  '235 - EAUX',                           2, 8.0, 22.1, 15.6, 35.2, 890.0,  118.3, 109.5),
  (3057640778901, '01 - EPICERIE',  '161 - PRODUITS POUR CHATS',            60, 0.0, 18.5, 3.4,  9.8,  145.0,  98.7,  91.2),
  (3057640889012, '01 - EPICERIE',  '160 - PRODUITS POUR CHIENS',           90, 0.0, 15.2, 2.8,  7.6,  112.0,  76.4,  71.8),
  (3057640990123, '02 - LIQUIDES',  '230 - WHISKIES,ALCOOLS,LIQUEURS,RHUM', 180, 0.0, 35.6, 4.1, 12.3, 180.0,  52.1,  48.9);

-- ─── Table logs_acces ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS logs_acces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    username VARCHAR(64),
    action VARCHAR(128) NOT NULL,
    detail VARCHAR(512),
    ip_address VARCHAR(45),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs_acces(timestamp DESC);

COMMIT;
PRAGMA foreign_keys = ON;

-- ─── Statistiques du dump ────────────────────────────────────────────────────
-- Table users    : 3 utilisateurs (comptes de test — mots de passe à réinitialiser)
-- Table produits : 10 produits de démonstration (jeu complet : ~8 500 produits)
-- Table logs_acces : vide à l'initialisation
--
-- Pour restaurer :
--   sqlite3 data/nondetention.db < nondetention_dump.sql
--
-- Pour voir le contenu :
--   sqlite3 data/nondetention.db "SELECT * FROM produits LIMIT 5;"
