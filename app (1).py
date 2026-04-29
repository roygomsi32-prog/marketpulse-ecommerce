import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime, date
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="MarketPulse CM — Collecte & Analyse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0d0d0d 0%, #1a1a1a 100%); border-right: 2px solid #FF6B00; }
[data-testid="stSidebar"] * { color: #f0f0f0 !important; }
[data-testid="stSidebar"] .stRadio > label { color: #FF6B00 !important; font-weight: 700; }
.stApp { background: #f7f3ee; }
.kpi-card { background: #0d0d0d; border-left: 4px solid #FF6B00; border-radius: 8px; padding: 18px 20px; margin-bottom: 10px; color: white; }
.kpi-card .kpi-value { font-size: 2rem; font-weight: 800; color: #FF6B00; font-family: 'Space Mono', monospace; }
.kpi-card .kpi-label { font-size: 0.78rem; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }
.hero-banner { background: linear-gradient(135deg, #0d0d0d 0%, #1f1f1f 60%, #FF6B00 100%); border-radius: 12px; padding: 32px 36px; margin-bottom: 28px; color: white; }
.hero-banner h1 { font-size: 2.4rem; font-weight: 800; margin: 0; letter-spacing: -1px; }
.hero-banner p  { font-size: 1rem; color: #ccc; margin-top: 6px; }
.hero-accent { color: #FF6B00; }
.form-section { background: white; border-radius: 10px; padding: 24px; margin-bottom: 18px; border: 1px solid #e0d8d0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.section-title { font-size: 1.1rem; font-weight: 700; color: #0d0d0d; border-left: 3px solid #FF6B00; padding-left: 10px; margin-bottom: 14px; }
.stButton > button { background: #FF6B00 !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; padding: 10px 28px !important; }
.stButton > button:hover { background: #e05a00 !important; transform: translateY(-1px); }
.stDownloadButton > button { background: #0d0d0d !important; color: white !important; border-radius: 8px !important; font-weight: 700 !important; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid #FF6B00; }
.stTabs [data-baseweb="tab"] { font-weight: 600; border-radius: 6px 6px 0 0; background: #e8e0d8; color: #555; }
.stTabs [aria-selected="true"] { background: #FF6B00 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()

with st.sidebar:
    st.markdown("## 📊 MarketPulse CM")
    st.markdown("*Plateforme de collecte & analyse*")
    st.markdown("---")
    page = st.radio("Navigation", [
        "🏠 Accueil",
        "📝 Saisie des données",
        "📂 Importer CSV",
        "📊 Analyse descriptive",
        "📈 Régression linéaire",
        "🔬 ACP (Réduction dim.)",
        "🤖 Clustering (K-Means)",
        "💾 Exporter les données",
    ])
    st.markdown("---")
    n = len(st.session_state.data)
    st.markdown(f"**Enregistrements :** `{n}`")
    if n > 0:
        cols_num = st.session_state.data.select_dtypes(include=np.number).columns.tolist()
        st.markdown(f"**Variables num. :** `{len(cols_num)}`")
    st.markdown("---")
    st.caption("INF 232 — EC2 · TP №1")

def hero(title, subtitle):
    st.markdown(f'<div class="hero-banner"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

def kpi_row(metrics):
    cols = st.columns(len(metrics))
    for col, (label, value, unit) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="kpi-card"><div class="kpi-value">{value}{unit}</div><div class="kpi-label">{label}</div></div>', unsafe_allow_html=True)

if page == "🏠 Accueil":
    hero("MarketPulse <span class='hero-accent'>CM</span>", "Application de collecte & analyse descriptive des données commerciales — Cameroun")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        <div class="form-section">
        <div class="section-title">🎯 Objectif de l'application</div>
        <p><b>MarketPulse CM</b> est une plateforme dédiée à la collecte structurée et à l'analyse
        des données commerciales des marchés camerounais.</p>
        <ul>
            <li>📝 Saisir des observations de vente, stock et prix en temps réel</li>
            <li>📊 Obtenir une analyse descriptive complète et automatique</li>
            <li>📈 Effectuer des régressions linéaires pour prédire les ventes</li>
            <li>🔬 Réduire la dimensionnalité avec l'ACP</li>
            <li>🤖 Découvrir des segments de produits via le clustering</li>
            <li>💾 Exporter les résultats en CSV</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="form-section">
        <div class="section-title">📋 Variables collectées</div>
        <table style="width:100%;font-size:0.85rem;">
            <tr><td>📦</td><td><b>Produit</b></td></tr>
            <tr><td>🏪</td><td><b>Type de commerce</b></td></tr>
            <tr><td>📍</td><td><b>Ville / Quartier</b></td></tr>
            <tr><td>💰</td><td><b>Prix unitaire (FCFA)</b></td></tr>
            <tr><td>🔢</td><td><b>Quantité vendue</b></td></tr>
            <tr><td>📦</td><td><b>Stock disponible</b></td></tr>
            <tr><td>💵</td><td><b>Chiffre d'affaires</b></td></tr>
            <tr><td>⭐</td><td><b>Satisfaction client</b></td></tr>
            <tr><td>📅</td><td><b>Date d'observation</b></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    st.info("👈 Utilisez le menu latéral pour naviguer. Commencez par **Saisie des données** ou **Importer CSV**.")

elif page == "📝 Saisie des données":
    hero("📝 Saisie des données", "Encodez une nouvelle observation commerciale")
    with st.form("saisie_form", clear_on_submit=True):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        section("🏪 Informations générales")
        c1, c2, c3 = st.columns(3)
        with c1:
            produit = st.text_input("Nom du produit *", placeholder="ex : Huile de palme 1L")
            type_commerce = st.selectbox("Type de commerce *", ["Boutique de quartier", "Grand marché", "Supermarché", "Grossiste", "Marché hebdomadaire", "Autre"])
        with c2:
            ville = st.selectbox("Ville *", ["Yaoundé", "Douala", "Bafoussam", "Garoua", "Maroua", "Ngaoundéré", "Bamenda", "Bertoua", "Ebolowa", "Autre"])
            quartier = st.text_input("Quartier / Zone", placeholder="ex : Mokolo, Mvog-Ada…")
        with c3:
            date_obs = st.date_input("Date d'observation *", value=date.today())
            categorie = st.selectbox("Catégorie de produit", ["Alimentation", "Boissons", "Hygiène / Cosmétique", "Textile / Habillement", "Électronique", "Quincaillerie", "Agriculture", "Autre"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        section("💰 Données économiques")
        c4, c5, c6 = st.columns(3)
        with c4:
            prix_unitaire = st.number_input("Prix unitaire (FCFA) *", min_value=0, step=50, value=500)
            cout_achat = st.number_input("Coût d'achat unitaire (FCFA)", min_value=0, step=50, value=350)
        with c5:
            qte_vendue = st.number_input("Quantité vendue (unités) *", min_value=0, step=1, value=10)
            stock_dispo = st.number_input("Stock disponible (unités)", min_value=0, step=1, value=50)
        with c6:
            satisfaction = st.slider("Satisfaction client (1–5) ⭐", 1, 5, 4)
            nb_concurrents = st.number_input("Nb de concurrents proches", min_value=0, step=1, value=2)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        section("📝 Observations complémentaires")
        observations = st.text_area("Remarques / contexte", placeholder="Promotions en cours, saisonnalité…", height=80)
        st.markdown("</div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✅ Enregistrer l'observation")
    if submitted:
        ca = prix_unitaire * qte_vendue
        marge = (prix_unitaire - cout_achat) * qte_vendue
        nouveau = {
            "date_observation": str(date_obs), "produit": produit, "categorie": categorie,
            "type_commerce": type_commerce, "ville": ville, "quartier": quartier,
            "prix_unitaire_fcfa": prix_unitaire, "cout_achat_fcfa": cout_achat,
            "quantite_vendue": qte_vendue, "stock_disponible": stock_dispo,
            "chiffre_affaires_fcfa": ca, "marge_brute_fcfa": marge,
            "satisfaction_client": satisfaction, "nb_concurrents": nb_concurrents,
            "observations": observations,
        }
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nouveau])], ignore_index=True)
        st.success(f"✅ Observation enregistrée ! CA : **{ca:,} FCFA** | Marge : **{marge:,} FCFA**")
        st.balloons()
    if not st.session_state.data.empty:
        section(f"📋 Données collectées ({len(st.session_state.data)} lignes)")
        st.dataframe(st.session_state.data, use_container_width=True)

elif page == "📂 Importer CSV":
    hero("📂 Importer un fichier CSV", "Chargez vos données existantes pour les analyser")
    template_data = {
        "date_observation": ["2024-01-15", "2024-01-15"],
        "produit": ["Huile palme 1L", "Savon OMO 500g"],
        "categorie": ["Alimentation", "Hygiène / Cosmétique"],
        "type_commerce": ["Boutique de quartier", "Grand marché"],
        "ville": ["Yaoundé", "Douala"],
        "quartier": ["Mokolo", "Akwa"],
        "prix_unitaire_fcfa": [800, 350],
        "cout_achat_fcfa": [600, 250],
        "quantite_vendue": [25, 40],
        "stock_disponible": [100, 60],
        "chiffre_affaires_fcfa": [20000, 14000],
        "marge_brute_fcfa": [5000, 4000],
        "satisfaction_client": [4, 5],
        "nb_concurrents": [3, 5],
        "observations": ["", "Promotion en cours"],
    }
    csv_template = pd.DataFrame(template_data).to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Télécharger le modèle CSV", data=csv_template, file_name="marketpulse_template.csv", mime="text/csv")
    uploaded = st.file_uploader("Glissez votre fichier CSV ici", type=["csv"])
    if uploaded:
        try:
            df_imp = pd.read_csv(uploaded)
            st.session_state.data = df_imp
            st.success(f"✅ {len(df_imp)} lignes importées avec succès !")
            st.dataframe(df_imp.head(10), use_container_width=True)
        except Exception as e:
            st.error(f"Erreur lors de l'import : {e}")

elif page == "📊 Analyse descriptive":
    hero("📊 Analyse descriptive", "Statistiques, distributions et visualisations automatiques")
    df = st.session_state.data
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible."); st.stop()
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    ca_total  = df["chiffre_affaires_fcfa"].sum() if "chiffre_affaires_fcfa" in df.columns else 0
    marge_tot = df["marge_brute_fcfa"].sum()      if "marge_brute_fcfa" in df.columns else 0
    qte_tot   = df["quantite_vendue"].sum()        if "quantite_vendue" in df.columns else 0
    sat_moy   = df["satisfaction_client"].mean()   if "satisfaction_client" in df.columns else 0
    kpi_row([
        ("Chiffre d'affaires total", f"{ca_total:,.0f}", " FCFA"),
        ("Marge brute totale",       f"{marge_tot:,.0f}", " FCFA"),
        ("Quantité totale vendue",   f"{int(qte_tot):,}", " u."),
        ("Satisfaction moyenne",     f"{sat_moy:.1f}", " ⭐"),
    ])
    tabs = st.tabs(["📋 Statistiques", "📊 Distributions", "🗺️ Géo-analyse", "🔗 Corrélations"])
    with tabs[0]:
        section("Statistiques descriptives — variables numériques")
        desc = df[num_cols].describe().T.round(2)
        desc["CV (%)"] = (desc["std"] / desc["mean"] * 100).round(1)
        st.dataframe(desc, use_container_width=True)
        section("Fréquences — variables catégorielles")
        if cat_cols:
            sel = st.selectbox("Variable", [c for c in cat_cols if c not in ["date_observation", "observations", "quartier"]])
            vc = df[sel].value_counts().reset_index()
            vc.columns = [sel, "Fréquence"]
            vc["Fréquence (%)"] = (vc["Fréquence"] / vc["Fréquence"].sum() * 100).round(1)
            st.dataframe(vc, use_container_width=True)
    with tabs[1]:
        section("Distribution d'une variable numérique")
        sel_num = st.selectbox("Variable numérique", num_cols)
        fig = px.histogram(df, x=sel_num, nbins=20, color_discrete_sequence=["#FF6B00"], title=f"Distribution de {sel_num}")
        fig.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4")
        st.plotly_chart(fig, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            if "ville" in df.columns and "chiffre_affaires_fcfa" in df.columns:
                fig2 = px.box(df, x="ville", y="chiffre_affaires_fcfa", color="ville", title="CA par ville", color_discrete_sequence=px.colors.qualitative.Set2)
                fig2.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4", showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)
        with c2:
            if "categorie" in df.columns and "quantite_vendue" in df.columns:
                agg = df.groupby("categorie")["quantite_vendue"].sum().reset_index()
                fig3 = px.pie(agg, names="categorie", values="quantite_vendue", title="Répartition des ventes par catégorie", color_discrete_sequence=px.colors.qualitative.Set3)
                fig3.update_layout(paper_bgcolor="#faf7f4")
                st.plotly_chart(fig3, use_container_width=True)
    with tabs[2]:
        if "ville" in df.columns:
            section("Chiffre d'affaires par ville")
            agg_ville = df.groupby("ville")[["chiffre_affaires_fcfa", "quantite_vendue", "marge_brute_fcfa"]].sum().reset_index()
            fig4 = px.bar(agg_ville, x="ville", y="chiffre_affaires_fcfa", color="chiffre_affaires_fcfa", color_continuous_scale=["#f7f3ee", "#FF6B00"], title="CA total par ville")
            fig4.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4")
            st.plotly_chart(fig4, use_container_width=True)
            if "type_commerce" in df.columns:
                section("CA par type de commerce et par ville")
                agg2 = df.groupby(["ville", "type_commerce"])["chiffre_affaires_fcfa"].sum().reset_index()
                fig5 = px.bar(agg2, x="ville", y="chiffre_affaires_fcfa", color="type_commerce", barmode="group", title="CA par ville & type de commerce")
                fig5.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4")
                st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("Ajoutez une colonne 'ville' pour voir l'analyse géographique.")
    with tabs[3]:
        section("Matrice de corrélation")
        if len(num_cols) >= 2:
            corr = df[num_cols].corr().round(2)
            fig6 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", title="Corrélations entre variables numériques", aspect="auto")
            fig6.update_layout(paper_bgcolor="#faf7f4")
            st.plotly_chart(fig6, use_container_width=True)
            section("Nuage de points")
            c1, c2 = st.columns(2)
            with c1:
                xv = st.selectbox("Axe X", num_cols, index=0)
            with c2:
                yv = st.selectbox("Axe Y", num_cols, index=min(1, len(num_cols)-1))
            color_col = st.selectbox("Couleur par", ["(aucune)"] + [c for c in cat_cols if c not in ["observations", "date_observation", "quartier"]])
            fig7 = px.scatter(df, x=xv, y=yv, color=None if color_col == "(aucune)" else color_col, trendline="ols", title=f"{yv} vs {xv}", color_discrete_sequence=px.colors.qualitative.Set2)
            fig7.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4")
            st.plotly_chart(fig7, use_container_width=True)

elif page == "📈 Régression linéaire":
    hero("📈 Régression linéaire", "Simple et multiple — prédire le chiffre d'affaires ou la marge")
    df = st.session_state.data
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible."); st.stop()
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    col1, col2 = st.columns(2)
    with col1:
        target = st.selectbox("Variable cible (Y)", num_cols, index=num_cols.index("chiffre_affaires_fcfa") if "chiffre_affaires_fcfa" in num_cols else 0)
    with col2:
        features = st.multiselect("Variables explicatives (X)", [c for c in num_cols if c != target], default=[c for c in ["prix_unitaire_fcfa", "quantite_vendue", "stock_disponible"] if c in num_cols and c != target])
    if st.button("🚀 Lancer la régression") and features:
        dfc = df[[target] + features].dropna()
        X = dfc[features].values
        y = dfc[target].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2     = 1 - ss_res / ss_tot
        rmse   = np.sqrt(np.mean((y - y_pred) ** 2))
        n, k   = len(y), len(features)
        r2_adj = 1 - (1 - r2) * (n - 1) / (n - k - 1)
        kpi_row([
            ("R²",        f"{r2:.4f}", ""),
            ("R² ajusté", f"{r2_adj:.4f}", ""),
            ("RMSE",      f"{rmse:,.0f}", " FCFA"),
            ("N obs.",    str(n), ""),
        ])
        section("Coefficients du modèle")
        coef_df = pd.DataFrame({
            "Variable": ["Constante"] + features,
            "Coefficient": [round(model.intercept_, 4)] + [round(c, 4) for c in model.coef_],
        })
        st.dataframe(coef_df, use_container_width=True)
        eq = f"**{target}** = {model.intercept_:.2f}"
        for f, c in zip(features, model.coef_):
            eq += f" + ({c:.4f}) × {f}"
        st.markdown(f"> 📐 **Équation :** {eq}")
        section("Valeurs réelles vs prédites")
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=y, mode="lines+markers", name="Réel", line=dict(color="#0d0d0d", width=2)))
        fig.add_trace(go.Scatter(y=y_pred, mode="lines", name="Prédit", line=dict(color="#FF6B00", width=2, dash="dash")))
        fig.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4", title="Réel vs Prédit", xaxis_title="Observation", yaxis_title=target)
        st.plotly_chart(fig, use_container_width=True)
        section("Résidus")
        fig2 = px.histogram(x=y - y_pred, nbins=20, color_discrete_sequence=["#FF6B00"], title="Distribution des résidus")
        fig2.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4", xaxis_title="Résidu", yaxis_title="Fréquence")
        st.plotly_chart(fig2, use_container_width=True)

elif page == "🔬 ACP (Réduction dim.)":
    hero("🔬 Analyse en Composantes Principales", "Réduction de la dimensionnalité des données")
    df = st.session_state.data
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible."); st.stop()
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    if len(num_cols) < 2:
        st.error("Il faut au moins 2 variables numériques."); st.stop()
    features = st.multiselect("Variables pour l'ACP", num_cols, default=num_cols)
    n_comp   = st.slider("Nombre de composantes", 2, min(len(features), 8), 2)
    if st.button("🔬 Lancer l'ACP") and len(features) >= 2:
        dfc  = df[features].dropna()
        X_sc = StandardScaler().fit_transform(dfc)
        pca  = PCA(n_components=n_comp)
        coords  = pca.fit_transform(X_sc)
        var_exp = pca.explained_variance_ratio_ * 100
        kpi_row([
            ("Variance expliquée (2 axes)", f"{sum(var_exp[:2]):.1f}", "%"),
            ("Variance totale expliquée",   f"{sum(var_exp):.1f}", "%"),
            ("N observations",              str(len(dfc)), ""),
            ("N variables",                 str(len(features)), ""),
        ])
        section("Variance expliquée par composante")
        fig1 = px.bar(x=[f"CP{i+1}" for i in range(n_comp)], y=var_exp, color=var_exp, color_continuous_scale=["#f7f3ee", "#FF6B00"], title="% de variance expliquée", labels={"x": "Composante", "y": "Variance (%)"})
        fig1.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4")
        st.plotly_chart(fig1, use_container_width=True)
        section("Projection des individus (CP1 vs CP2)")
        cat_cols = [c for c in df.columns if df[c].dtype == object and c not in ["observations", "date_observation", "quartier"]]
        color_col = None
        if cat_cols:
            color_var = st.selectbox("Colorier par", ["(aucune)"] + cat_cols)
            if color_var != "(aucune)":
                color_col = df.loc[dfc.index, color_var]
        df_pca = pd.DataFrame(coords[:, :2], columns=["CP1", "CP2"])
        if color_col is not None:
            df_pca["groupe"] = color_col.values
            fig2 = px.scatter(df_pca, x="CP1", y="CP2", color="groupe", title="Individus — CP1 vs CP2", color_discrete_sequence=px.colors.qualitative.Set2)
        else:
            fig2 = px.scatter(df_pca, x="CP1", y="CP2", title="Individus — CP1 vs CP2", color_discrete_sequence=["#FF6B00"])
        fig2.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4")
        st.plotly_chart(fig2, use_container_width=True)
        section("Cercle des corrélations")
        loadings = pca.components_.T
        fig3 = go.Figure()
        for i, feat in enumerate(features):
            fig3.add_trace(go.Scatter(x=[0, loadings[i, 0]], y=[0, loadings[i, 1]], mode="lines+markers+text", text=["", feat], textposition="top center", line=dict(color="#FF6B00", width=2), marker=dict(size=[0, 10], color="#0d0d0d"), showlegend=False))
        theta = np.linspace(0, 2 * np.pi, 100)
        fig3.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode="lines", line=dict(color="#ccc"), showlegend=False))
        fig3.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4", title="Cercle des corrélations", xaxis=dict(title="CP1", range=[-1.2, 1.2], zeroline=True, zerolinecolor="#999"), yaxis=dict(title="CP2", range=[-1.2, 1.2], zeroline=True, zerolinecolor="#999", scaleanchor="x", scaleratio=1))
        st.plotly_chart(fig3, use_container_width=True)

elif page == "🤖 Clustering (K-Means)":
    hero("🤖 Clustering K-Means", "Segmentation automatique des produits / observations")
    df = st.session_state.data
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible."); st.stop()
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    features = st.multiselect("Variables de clustering", num_cols, default=[c for c in ["prix_unitaire_fcfa", "quantite_vendue", "chiffre_affaires_fcfa"] if c in num_cols])
    k = st.slider("Nombre de clusters (K)", 2, 8, 3)
    if st.button("🤖 Lancer le K-Means") and len(features) >= 2:
        dfc      = df[features].dropna()
        X_sc     = StandardScaler().fit_transform(dfc)
        labels   = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X_sc)
        inertias = [KMeans(n_clusters=ki, random_state=42, n_init=10).fit(X_sc).inertia_ for ki in range(1, 10)]
        section("Méthode du coude (Elbow Method)")
        fig1 = px.line(x=list(range(1, 10)), y=inertias, markers=True, title="Inertie en fonction du nombre de clusters", labels={"x": "K", "y": "Inertie"}, color_discrete_sequence=["#FF6B00"])
        fig1.add_vline(x=k, line_dash="dash", line_color="#0d0d0d", annotation_text=f"K={k} choisi")
        fig1.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4")
        st.plotly_chart(fig1, use_container_width=True)
        section(f"Visualisation des {k} clusters")
        df_cl = dfc.copy()
        df_cl["Cluster"] = [f"Cluster {i+1}" for i in labels]
        fig2 = px.scatter(df_cl, x=features[0], y=features[1], color="Cluster", title=f"Segmentation K-Means (K={k})", color_discrete_sequence=px.colors.qualitative.Set2, hover_data=features)
        fig2.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4")
        st.plotly_chart(fig2, use_container_width=True)
        section("Profil moyen par cluster")
        st.dataframe(df_cl.groupby("Cluster")[features].mean().round(2), use_container_width=True)
        section("Distribution par cluster")
        counts = df_cl["Cluster"].value_counts().reset_index()
        counts.columns = ["Cluster", "N observations"]
        fig3 = px.bar(counts, x="Cluster", y="N observations", color="Cluster", color_discrete_sequence=px.colors.qualitative.Set2, title="Effectif par cluster")
        fig3.update_layout(plot_bgcolor="#faf7f4", paper_bgcolor="#faf7f4", showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

elif page == "💾 Exporter les données":
    hero("💾 Exporter les données", "Téléchargez vos données collectées en CSV")
    df = st.session_state.data
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible."); st.stop()
    st.dataframe(df, use_container_width=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(label="⬇️ Télécharger en CSV", data=df.to_csv(index=False).encode("utf-8"), file_name=f"marketpulse_data_{ts}.csv", mime="text/csv")
    section("Résumé du jeu de données")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"- **Lignes :** {len(df)}")
        st.markdown(f"- **Colonnes :** {len(df.columns)}")
        st.markdown(f"- **Variables numériques :** {len(df.select_dtypes(include=np.number).columns)}")
    with col2:
        st.markdown(f"- **Valeurs manquantes :** {df.isnull().sum().sum()}")
        if "date_observation" in df.columns:
            st.markdown(f"- **Période :** {df['date_observation'].min()} → {df['date_observation'].max()}")
