import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, date
import uuid
import json

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MarketPulse — E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 { font-family: 'Syne', sans-serif; }

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e8e6f0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111118;
    border-right: 1px solid #222230;
}

/* Cards */
.metric-card {
    background: linear-gradient(135deg, #16161f 0%, #1e1e2e 100%);
    border: 1px solid #2a2a40;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #ff6b35, #f7c59f);
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #ff6b35;
    line-height: 1;
}
.metric-label {
    font-size: 0.78rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 6px;
}
.metric-delta {
    font-size: 0.85rem;
    color: #4ecdc4;
    margin-top: 4px;
}

/* Section header */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #e8e6f0;
    border-left: 4px solid #ff6b35;
    padding-left: 14px;
    margin: 32px 0 20px 0;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background: #16161f !important;
    border: 1px solid #2a2a40 !important;
    color: #e8e6f0 !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #ff6b35, #ff8c5a);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    padding: 0.6rem 2rem;
    transition: all 0.2s;
    box-shadow: 0 4px 20px rgba(255,107,53,0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(255,107,53,0.45);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #111118;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #888;
    border-radius: 8px;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: #ff6b35 !important;
    color: white !important;
}

/* Success / info boxes */
.stSuccess { background: #0d2b22 !important; border-color: #4ecdc4 !important; }
.stInfo    { background: #0d1a2b !important; }

/* Dataframe */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* Hero */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ff6b35 0%, #f7c59f 60%, #4ecdc4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 8px;
}
.hero-sub {
    color: #888;
    font-size: 1rem;
    margin-bottom: 32px;
}
</style>
""", unsafe_allow_html=True)

# ── Data persistence (CSV) ─────────────────────────────────────────────────────
DATA_FILE = "data/transactions.csv"
os.makedirs("data", exist_ok=True)

COLUMNS = [
    "id", "date", "product_name", "category", "quantity",
    "unit_price", "total_revenue", "region", "channel",
    "customer_type", "payment_method", "return_flag", "timestamp"
]

CATEGORIES = ["Électronique", "Mode & Vêtements", "Alimentation", "Maison & Jardin",
               "Beauté & Santé", "Sports & Loisirs", "Livres & Médias", "Jouets & Enfants"]
REGIONS    = ["Centre", "Littoral", "Nord", "Sud", "Est", "Ouest", "Adamaoua", "Extrême-Nord"]
CHANNELS   = ["Site web", "Application mobile", "Marketplace", "Réseaux sociaux", "Boutique physique"]
CUST_TYPES = ["Nouveau client", "Client fidèle", "Client premium", "Client professionnel"]
PAYMENTS   = ["Mobile Money", "Carte bancaire", "Virement", "Paiement à la livraison", "Crypto"]

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=["date", "timestamp"])
        return df
    return pd.DataFrame(columns=COLUMNS)

def save_record(record: dict):
    df = load_data()
    new_row = pd.DataFrame([record])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def generate_demo_data(n=80):
    np.random.seed(42)
    dates   = pd.date_range(end=date.today(), periods=n, freq='D')
    records = []
    for d in dates:
        qty   = np.random.randint(1, 50)
        price = round(np.random.uniform(500, 150_000), 0)
        records.append({
            "id":             str(uuid.uuid4())[:8],
            "date":           d,
            "product_name":   np.random.choice(
                ["iPhone 15", "Samsung TV", "Sneakers Nike", "Sac à main", "Riz premium",
                 "Laptop Dell", "Parfum Dior", "Livre Python", "Ballon foot", "Casque BT"]),
            "category":       np.random.choice(CATEGORIES),
            "quantity":       qty,
            "unit_price":     price,
            "total_revenue":  round(qty * price, 0),
            "region":         np.random.choice(REGIONS),
            "channel":        np.random.choice(CHANNELS),
            "customer_type":  np.random.choice(CUST_TYPES),
            "payment_method": np.random.choice(PAYMENTS),
            "return_flag":    np.random.choice(["Non", "Oui"], p=[0.88, 0.12]),
            "timestamp":      datetime.now(),
        })
    pd.DataFrame(records).to_csv(DATA_FILE, index=False)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:Syne;font-size:1.5rem;font-weight:800;color:#ff6b35;">🛒 MarketPulse</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#888;font-size:0.8rem;">E-Commerce Analytics Platform</p>', unsafe_allow_html=True)
    st.divider()

    page = st.radio(
        "Navigation",
        ["🏠 Tableau de bord", "➕ Saisir une vente", "📊 Analyse descriptive", "📋 Données brutes"],
        label_visibility="collapsed"
    )

    st.divider()
    df_all = load_data()
    st.markdown(f'<p style="color:#888;font-size:0.78rem;">📦 {len(df_all)} transactions enregistrées</p>', unsafe_allow_html=True)

    if st.button("🎲 Générer données démo"):
        generate_demo_data()
        st.success("80 transactions générées !")
        st.rerun()

    if len(df_all) > 0:
        csv_bytes = df_all.to_csv(index=False).encode()
        st.download_button("⬇️ Exporter CSV", csv_bytes, "marketpulse_data.csv", "text/csv")

    st.divider()
    st.markdown('<p style="color:#555;font-size:0.72rem;">INF 232 EC2 · TP #1 · 2026</p>', unsafe_allow_html=True)

# ── Reload after nav ───────────────────────────────────────────────────────────
df = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Tableau de bord":
    st.markdown('<div class="hero-title">MarketPulse Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Collecte & analyse descriptive des données e-commerce en temps réel</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("📭 Aucune donnée. Utilisez le bouton **'Générer données démo'** dans la barre latérale, ou saisissez des ventes manuellement.")
    else:
        df["total_revenue"] = pd.to_numeric(df["total_revenue"], errors="coerce")
        df["quantity"]      = pd.to_numeric(df["quantity"], errors="coerce")
        df["date"]          = pd.to_datetime(df["date"], errors="coerce")

        total_rev  = df["total_revenue"].sum()
        total_qty  = df["quantity"].sum()
        n_trans    = len(df)
        avg_basket = df["total_revenue"].mean()
        return_rate = (df["return_flag"] == "Oui").mean() * 100 if "return_flag" in df.columns else 0

        # KPI row
        c1, c2, c3, c4, c5 = st.columns(5)
        kpis = [
            (c1, f"{total_rev:,.0f} XAF", "Chiffre d'affaires", ""),
            (c2, f"{n_trans}", "Transactions", ""),
            (c3, f"{total_qty:,.0f}", "Unités vendues", ""),
            (c4, f"{avg_basket:,.0f} XAF", "Panier moyen", ""),
            (c5, f"{return_rate:.1f}%", "Taux de retour", ""),
        ]
        for col, val, label, delta in kpis:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{val}</div>
                    <div class="metric-label">{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-title">Évolution du chiffre d\'affaires</div>', unsafe_allow_html=True)
        daily = df.groupby(df["date"].dt.date)["total_revenue"].sum().reset_index()
        daily.columns = ["date", "revenue"]
        fig_line = px.area(daily, x="date", y="revenue",
                           color_discrete_sequence=["#ff6b35"],
                           template="plotly_dark")
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=0,b=0), font_color="#e8e6f0",
            xaxis=dict(gridcolor="#1e1e2e"), yaxis=dict(gridcolor="#1e1e2e")
        )
        fig_line.update_traces(fillcolor="rgba(255,107,53,0.15)", line_width=2)
        st.plotly_chart(fig_line, use_container_width=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('<div class="section-title">Ventes par catégorie</div>', unsafe_allow_html=True)
            cat_rev = df.groupby("category")["total_revenue"].sum().reset_index().sort_values("total_revenue", ascending=True)
            fig_bar = px.bar(cat_rev, x="total_revenue", y="category", orientation="h",
                             color="total_revenue", color_continuous_scale=["#1e1e2e","#ff6b35"],
                             template="plotly_dark")
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=0,r=0,t=0,b=0), showlegend=False,
                                  coloraxis_showscale=False, font_color="#e8e6f0",
                                  yaxis=dict(gridcolor="#1e1e2e"), xaxis=dict(gridcolor="#1e1e2e"))
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_r:
            st.markdown('<div class="section-title">Canaux de vente</div>', unsafe_allow_html=True)
            ch_rev = df.groupby("channel")["total_revenue"].sum().reset_index()
            fig_pie = px.pie(ch_rev, values="total_revenue", names="channel",
                             color_discrete_sequence=["#ff6b35","#f7c59f","#4ecdc4","#45b7d1","#96ceb4"],
                             template="plotly_dark", hole=0.55)
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=0,r=0,t=0,b=0), font_color="#e8e6f0",
                                  legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_pie, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — FORMULAIRE DE SAISIE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Saisir une vente":
    st.markdown('<div class="hero-title">Nouvelle transaction</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Enregistrez une vente dans la base de données</div>', unsafe_allow_html=True)

    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            prod_name  = st.text_input("🏷️ Nom du produit", placeholder="ex: iPhone 15 Pro")
            category   = st.selectbox("📂 Catégorie", CATEGORIES)
            quantity   = st.number_input("📦 Quantité", min_value=1, max_value=10000, value=1)
            unit_price = st.number_input("💰 Prix unitaire (XAF)", min_value=0, value=5000, step=100)
        with c2:
            sale_date   = st.date_input("📅 Date de la vente", value=date.today())
            region      = st.selectbox("🗺️ Région", REGIONS)
            channel     = st.selectbox("📡 Canal de vente", CHANNELS)
            cust_type   = st.selectbox("👤 Type de client", CUST_TYPES)
            payment     = st.selectbox("💳 Mode de paiement", PAYMENTS)
            return_flag = st.selectbox("↩️ Retour produit", ["Non", "Oui"])

    total = quantity * unit_price
    st.markdown(f"""
    <div class="metric-card" style="max-width:320px;margin-top:16px;">
        <div class="metric-label">Montant total calculé</div>
        <div class="metric-value">{total:,.0f} XAF</div>
    </div>""", unsafe_allow_html=True)

    if st.button("✅ Enregistrer la transaction"):
        if not prod_name.strip():
            st.error("Veuillez saisir un nom de produit.")
        else:
            record = {
                "id":             str(uuid.uuid4())[:8],
                "date":           str(sale_date),
                "product_name":   prod_name.strip(),
                "category":       category,
                "quantity":       quantity,
                "unit_price":     unit_price,
                "total_revenue":  total,
                "region":         region,
                "channel":        channel,
                "customer_type":  cust_type,
                "payment_method": payment,
                "return_flag":    return_flag,
                "timestamp":      str(datetime.now()),
            }
            save_record(record)
            st.success(f"✅ Transaction **{record['id']}** enregistrée avec succès !")
            st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — ANALYSE DESCRIPTIVE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Analyse descriptive":
    st.markdown('<div class="hero-title">Analyse descriptive</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Statistiques complètes sur vos données de vente</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("Aucune donnée disponible. Générez des données démo ou saisissez des ventes.")
    else:
        df["total_revenue"] = pd.to_numeric(df["total_revenue"], errors="coerce")
        df["unit_price"]    = pd.to_numeric(df["unit_price"], errors="coerce")
        df["quantity"]      = pd.to_numeric(df["quantity"], errors="coerce")

        tab1, tab2, tab3, tab4 = st.tabs(["📈 Statistiques", "🗺️ Régions", "📦 Produits", "💳 Paiements"])

        with tab1:
            st.markdown('<div class="section-title">Statistiques descriptives</div>', unsafe_allow_html=True)
            stats = df[["quantity","unit_price","total_revenue"]].describe().round(2)
            stats.index = ["Nb obs.", "Moyenne", "Écart-type", "Min", "Q25%", "Médiane", "Q75%", "Max"]
            st.dataframe(stats.style.background_gradient(cmap="Oranges"), use_container_width=True)

            st.markdown('<div class="section-title">Distribution du chiffre d\'affaires</div>', unsafe_allow_html=True)
            fig_hist = px.histogram(df, x="total_revenue", nbins=25,
                                    color_discrete_sequence=["#ff6b35"], template="plotly_dark",
                                    labels={"total_revenue": "CA (XAF)", "count": "Fréquence"})
            fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   margin=dict(l=0,r=0,t=0,b=0), font_color="#e8e6f0",
                                   xaxis=dict(gridcolor="#1e1e2e"), yaxis=dict(gridcolor="#1e1e2e"))
            st.plotly_chart(fig_hist, use_container_width=True)

            st.markdown('<div class="section-title">Corrélation Quantité × Prix unitaire</div>', unsafe_allow_html=True)
            fig_sc = px.scatter(df, x="quantity", y="unit_price", color="category",
                                size="total_revenue", template="plotly_dark",
                                color_discrete_sequence=px.colors.qualitative.Bold,
                                labels={"quantity":"Quantité","unit_price":"Prix unitaire (XAF)"})
            fig_sc.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                 margin=dict(l=0,r=0,t=0,b=0), font_color="#e8e6f0",
                                 xaxis=dict(gridcolor="#1e1e2e"), yaxis=dict(gridcolor="#1e1e2e"))
            st.plotly_chart(fig_sc, use_container_width=True)

        with tab2:
            st.markdown('<div class="section-title">Chiffre d\'affaires par région</div>', unsafe_allow_html=True)
            reg = df.groupby("region").agg(
                CA=("total_revenue","sum"),
                Transactions=("id","count"),
                Panier_moyen=("total_revenue","mean")
            ).reset_index().sort_values("CA", ascending=False)
            reg["CA"] = reg["CA"].round(0)
            reg["Panier_moyen"] = reg["Panier_moyen"].round(0)
            fig_reg = px.bar(reg, x="region", y="CA", color="CA",
                             color_continuous_scale=["#1e1e2e","#ff6b35"],
                             template="plotly_dark")
            fig_reg.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=0,r=0,t=0,b=0), font_color="#e8e6f0",
                                  coloraxis_showscale=False,
                                  xaxis=dict(gridcolor="#1e1e2e"), yaxis=dict(gridcolor="#1e1e2e"))
            st.plotly_chart(fig_reg, use_container_width=True)
            st.dataframe(reg.style.background_gradient(subset=["CA"], cmap="Oranges"), use_container_width=True)

        with tab3:
            st.markdown('<div class="section-title">Top 10 produits</div>', unsafe_allow_html=True)
            top = df.groupby("product_name")["total_revenue"].sum().nlargest(10).reset_index()
            top.columns = ["Produit", "CA total (XAF)"]
            fig_top = px.bar(top, x="CA total (XAF)", y="Produit", orientation="h",
                             color="CA total (XAF)", color_continuous_scale=["#1e1e2e","#4ecdc4"],
                             template="plotly_dark")
            fig_top.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=0,r=0,t=0,b=0), font_color="#e8e6f0",
                                  coloraxis_showscale=False,
                                  yaxis=dict(gridcolor="#1e1e2e"), xaxis=dict(gridcolor="#1e1e2e"))
            st.plotly_chart(fig_top, use_container_width=True)

        with tab4:
            st.markdown('<div class="section-title">Répartition des modes de paiement</div>', unsafe_allow_html=True)
            pay = df.groupby("payment_method")["total_revenue"].sum().reset_index()
            fig_pay = px.bar(pay, x="payment_method", y="total_revenue",
                             color="payment_method", template="plotly_dark",
                             color_discrete_sequence=["#ff6b35","#f7c59f","#4ecdc4","#45b7d1","#96ceb4"])
            fig_pay.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=0,r=0,t=0,b=0), font_color="#e8e6f0",
                                  showlegend=False,
                                  xaxis=dict(gridcolor="#1e1e2e"), yaxis=dict(gridcolor="#1e1e2e"))
            st.plotly_chart(fig_pay, use_container_width=True)

            ct = df.groupby("customer_type")["total_revenue"].sum().reset_index()
            fig_ct = px.pie(ct, values="total_revenue", names="customer_type", hole=0.5,
                            color_discrete_sequence=["#ff6b35","#f7c59f","#4ecdc4","#45b7d1"],
                            template="plotly_dark")
            fig_ct.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e8e6f0",
                                 margin=dict(l=0,r=0,t=20,b=0),
                                 legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_ct, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — DONNÉES BRUTES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Données brutes":
    st.markdown('<div class="hero-title">Données brutes</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Visualisez et filtrez toutes les transactions enregistrées</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("Aucune donnée disponible.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            cats_sel = st.multiselect("Filtrer par catégorie", df["category"].unique(), default=list(df["category"].unique()))
        with c2:
            reg_sel  = st.multiselect("Filtrer par région", df["region"].unique(), default=list(df["region"].unique()))
        with c3:
            ch_sel   = st.multiselect("Filtrer par canal", df["channel"].unique(), default=list(df["channel"].unique()))

        filtered = df[
            df["category"].isin(cats_sel) &
            df["region"].isin(reg_sel) &
            df["channel"].isin(ch_sel)
        ]

        st.markdown(f'<p style="color:#888;font-size:0.85rem;">{len(filtered)} enregistrements affichés</p>', unsafe_allow_html=True)
        st.dataframe(filtered.drop(columns=["timestamp"], errors="ignore"), use_container_width=True, height=500)
