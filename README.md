# 📊 MarketPulse CM — Application de collecte & analyse des données commerciales

> **INF 232 – EC2 | TP №1 | Analyse de données**

## 🎯 Description

**MarketPulse CM** est une application web interactive développée en Python avec Streamlit, dédiée à la **collecte** et à l'**analyse descriptive** des données commerciales des marchés camerounais.

### Fonctionnalités
| Module | Description |
|---|---|
| 📝 Saisie des données | Formulaire structuré pour encoder les observations de marché |
| 📂 Importer CSV | Charger des données existantes + modèle téléchargeable |
| 📊 Analyse descriptive | Statistiques, distributions, corrélations, analyse géographique |
| 📈 Régression linéaire | Simple et multiple avec visualisation des résidus |
| 🔬 ACP | Réduction de dimensionnalité + cercle des corrélations |
| 🤖 Clustering K-Means | Segmentation automatique + méthode du coude |
| 💾 Export CSV | Téléchargement des données collectées |

---

## 🚀 Déploiement sur Streamlit Cloud (GRATUIT)

### Étape 1 — Pré-requis
- Compte GitHub (gratuit) : https://github.com
- Compte Streamlit Cloud (gratuit) : https://streamlit.io/cloud

### Étape 2 — Créer un dépôt GitHub

```bash
# Clonez ou créez un nouveau repo GitHub
git init marketpulse
cd marketpulse

# Copiez les fichiers :
#   app.py
#   requirements.txt
#   README.md

git add .
git commit -m "Initial commit - MarketPulse CM"
git remote add origin https://github.com/VOTRE_USERNAME/marketpulse-cm.git
git push -u origin main
```

### Étape 3 — Déployer sur Streamlit Cloud

1. Allez sur https://share.streamlit.io
2. Cliquez **"New app"**
3. Sélectionnez votre dépôt GitHub
4. **Main file path** : `app.py`
5. Cliquez **"Deploy!"**

✅ Votre app sera disponible à une URL du type :
```
https://VOTRE_USERNAME-marketpulse-cm-app-XXXX.streamlit.app
```

---

## 💻 Exécution locale

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
streamlit run app.py

# L'app s'ouvre automatiquement sur http://localhost:8501
```

---

## 📋 Variables collectées

| Variable | Type | Description |
|---|---|---|
| date_observation | Date | Date de l'observation |
| produit | Texte | Nom du produit |
| categorie | Catégorielle | Catégorie de produit |
| type_commerce | Catégorielle | Type de point de vente |
| ville | Catégorielle | Ville d'observation |
| quartier | Texte | Quartier ou zone |
| prix_unitaire_fcfa | Numérique | Prix de vente unitaire |
| cout_achat_fcfa | Numérique | Coût d'achat unitaire |
| quantite_vendue | Numérique | Quantité vendue |
| stock_disponible | Numérique | Stock disponible |
| chiffre_affaires_fcfa | Numérique | CA calculé automatiquement |
| marge_brute_fcfa | Numérique | Marge calculée automatiquement |
| satisfaction_client | Numérique | Note de 1 à 5 |
| nb_concurrents | Numérique | Nombre de concurrents proches |
| observations | Texte | Remarques libres |

---

## 🛠️ Technologies

- **Python 3.10+**
- **Streamlit** — Interface web
- **Pandas / NumPy** — Manipulation des données
- **Plotly** — Visualisations interactives
- **Scikit-learn** — Régression, ACP, K-Means

---

## 📊 Critères pédagogiques couverts

| Critère | Éléments |
|---|---|
| 💡 Idée & créativité | Secteur Commerce/Marché camerounais, KPIs FCFA, villes du Cameroun |
| 🔒 Robustesse | Gestion des valeurs manquantes, validations, try/catch import |
| ⚡ Efficacité | Calculs automatiques CA/Marge, analyse en 1 clic |
| ✅ Fiabilité | sklearn pour les modèles, Plotly pour les graphiques |

---

*Cours INF 232 EC2 — TP №1 — Développé avec Python & Streamlit*
