import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import warnings
warnings.filterwarnings("ignore")

# PAGE CONFIG
st.set_page_config(
    page_title="VesselOptima Hub",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

#THEME & GLOBAL CSS (BG & SLIDER) 
SEA_BG_URL = "https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?q=80&w=1925&auto=format&fit=crop"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght=700;900&family=DM+Sans:wght=300;400;500;600&display=swap');

:root {{
    --deep:    #060b19;
    --teal:    #2a9d8f;
    --foam:    #84d8c4;
    --coral:   #ff8fa3;
    --white:   #f0f6ff;
    --muted:   #8899bb;
}}

html, body, [data-testid="stAppViewContainer"] {{
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif !important;
}}

[data-testid="stAppViewContainer"] {{
    background-image: linear-gradient(to bottom, rgba(6, 11, 25, 0.85), rgba(10, 20, 45, 0.95)), url("{SEA_BG_URL}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}

[data-testid="stSidebar"] {{
    background: rgba(6, 11, 25, 0.45) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}}

[data-testid="stSidebar"] * {{
    color: var(--white) !important;
}}

[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {{
    background: rgba(255, 255, 255, 0.1) !important;
    height: 6px !important;
    border-radius: 3px !important;
}}

[data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] > div {{
    background: transparent !important;
}}

[data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] button {{
    background-color: var(--coral) !important;
    border: 2px solid var(--white) !important;
    box-shadow: 0 0 8px var(--coral) !important;
    width: 16px !important;
    height: 16px !important;
}}

[data-testid="stTabs"] [role="tablist"] {{
    background: rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(8px);
    border-radius: 14px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    gap: 2px !important;
}}

[data-testid="stTabs"] [role="tab"] {{
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 8px 16px !important;
    transition: all 0.2s !important;
}}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    background: linear-gradient(135deg, #1a6b8a, #2a9d8f) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(42,157,143,0.3) !important;
}}

[data-testid="stButton"] > button {{
    background: linear-gradient(135deg, #2a9d8f 0%, #1a6b8a 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    box-shadow: 0 4px 20px rgba(42,157,143,0.2) !important;
}}

[data-testid="stButton"] > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(42,157,143,0.4) !important;
}}

[data-testid="stDataFrame"] {{
    border-radius: 14px !important;
    background: rgba(6, 11, 25, 0.6) !important;
}}

[data-testid="metric-container"] {{
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
}}

[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: var(--foam) !important;
    font-family: 'Playfair Display', serif !important;
}}

h1, h2, h3 {{
    font-family: 'Playfair Display', serif !important;
}}
</style>
""", unsafe_allow_html=True)

# HELPERS
def set_plot_style():
    plt.rcParams.update({
        "figure.facecolor":  "#060b19",
        "axes.facecolor":    "#060b19",
        "axes.edgecolor":    "#1a3060",
        "axes.labelcolor":   "#8899bb",
        "xtick.color":       "#8899bb",
        "ytick.color":       "#8899bb",
        "text.color":        "#f0f6ff",
        "grid.color":        "#1a3060",
        "grid.alpha":        0.4,
    })

set_plot_style()

# HERO BANNER
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(6,11,25,0.75) 0%, rgba(26,107,138,0.6) 50%, rgba(42,157,143,0.3) 100%);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 22px;
    padding: 36px 40px;
    margin-bottom: 28px;
">
  <p style="color:#84d8c4; font-size:0.78rem; letter-spacing:3px; text-transform:uppercase; margin:0 0 8px;">
    Sistem Pendukung Keputusan Otoritas Pelabuhan Internasional
  </p>
  <h1 style="
      font-size:2.6rem; font-weight:900; margin:0 0 10px;
      background: linear-gradient(90deg, #f0f6ff 0%, #84d8c4 60%, #ff8fa3 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  ">VesselOptima Hub</h1>
  <p style="color:#8899bb; font-size:0.95rem; margin:0;">
    Seleksi Otomatis Pelayaran Kapal Terbaik untuk Prioritas Sandar Dermaga &nbsp;|&nbsp;
    <span style="color:#84d8c4;">Fuzzy Standard Logic</span>
  </p>
</div>
""", unsafe_allow_html=True)

# DATA LOADING
@st.cache_data
def load_data():
    try:
        df_raw = pd.read_csv("Ship_Performance_Dataset.csv")
        return df_raw.dropna()
    except FileNotFoundError:
        np.random.seed(42)
        n_data = 300
        return pd.DataFrame({
            "Ship_Type": np.random.choice(["Container Ship", "Fish Carrier", "Bulk Carrier", "Tanker"], n_data),
            "Route_Type": np.random.choice(["Coastal", "Short-haul", "Long-haul", "Transoceanic"], n_data),
            "Speed_Over_Ground_knots": np.random.uniform(9, 22, n_data),
            "Cargo_Weight_tons": np.random.uniform(1000, 50000, n_data),
            "Revenue_per_Voyage_USD": np.random.uniform(150000, 800000, n_data),
            "Operational_Cost_USD": np.random.uniform(100000, 500000, n_data),
            "Turnaround_Time_hours": np.random.uniform(12, 96, n_data)
        })

df = load_data()

CRITERIA = {
    "Speed_Over_Ground_knots":  {"label": "Kecepatan (knots)",   "benefit": True},
    "Cargo_Weight_tons":        {"label": "Bobot Kargo (ton)",   "benefit": True},
    "Revenue_per_Voyage_USD":   {"label": "Revenue Finansial (USD)", "benefit": True},
    "Operational_Cost_USD":     {"label": "Biaya Operasional (USD)", "benefit": False},
    "Turnaround_Time_hours":    {"label": "Waktu Tambat (jam)", "benefit": False},
}
CRIT_KEYS = list(CRITERIA.keys())

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 24px;">
        <div style="font-family:'Playfair Display',serif; font-size:1.6rem; font-weight:900; background:linear-gradient(90deg,#84d8c4,#ff8fa3); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">VesselOptima</div>
        <div style="color:#8899bb; font-size:0.72rem; letter-spacing:2.5px; text-transform:uppercase; margin-top:4px;">Port Control Center</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.1); margin:0 0 20px;">
    """, unsafe_allow_html=True)

    st.markdown('<p style="color:#84d8c4; font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">Bobot Pengaruh Kriteria</p>', unsafe_allow_html=True)
    w_speed = st.slider("Kecepatan Kapal", 0.0, 1.0, 0.20, 0.05)
    w_cargo = st.slider("Kapasitas Muatan", 0.0, 1.0, 0.20, 0.05)
    w_rev   = st.slider("Revenue Keuntungan", 0.0, 1.0, 0.20, 0.05)
    w_cost  = st.slider("Efisiensi Biaya", 0.0, 1.0, 0.20, 0.05)
    w_turn  = st.slider("Efisiensi Waktu Sandar", 0.0, 1.0, 0.20, 0.05)

    total_w = w_speed + w_cargo + w_rev + w_cost + w_turn
    is_weight_valid = abs(total_w - 1.0) < 0.01

    if is_weight_valid:
        st.markdown(f'<p style="color:#84d8c4; font-size:0.82rem; margin-top:5px;">Total bobot: <b>{total_w:.2f} (Valid)</b></p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p style="color:#ff8fa3; font-size:0.82rem; margin-top:5px;">Total bobot: <b>{total_w:.2f} (Harus = 1.00)</b></p>', unsafe_allow_html=True)

    st.markdown('<hr style="border-color:rgba(255,255,255,0.1); margin:16px 0;">', unsafe_allow_html=True)
    st.markdown('<p style="color:#84d8c4; font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">Filter Kunjungan</p>', unsafe_allow_html=True)
    
    top_n = st.number_input("Tampilkan Top Kapal", min_value=5, max_value=50, value=15, step=5)
    ship_filter = st.selectbox("Jenis Kapal Kargo", ["Semua"] + sorted(df["Ship_Type"].dropna().astype(str).unique().tolist()))
    route_filter = st.selectbox("Zona Rute Sandar", ["Semua"] + sorted(df["Route_Type"].dropna().astype(str).unique().tolist()))

    st.markdown('<hr style="border-color:rgba(255,255,255,0.1); margin:16px 0;">', unsafe_allow_html=True)
    run = st.button("Jalankan Seleksi Fuzzy", use_container_width=True, disabled=not is_weight_valid)

# TABS LAYOUT
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Log Kunjungan Pelabuhan",
    "Kurva Keanggotaan Fuzzy",
    "Konfigurasi Aturan",
    "Hasil Rekomendasi Kapal",
    "Tim Pengembang"
])


# TAB 1 — LOG KUNJUNGAN PELABUHAN
with tab1:
    st.markdown("### Log Histori Kedatangan Kapal")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Total Pelayaran Terdata", f"{len(df):,}")
    col_m2.metric("Kategori Kapal", df["Ship_Type"].nunique())
    col_m3.metric("Rata-rata Muatan", f"{df['Cargo_Weight_tons'].mean():,.1f} ton")
    col_m4.metric("Rata-rata Waktu Sandar", f"{df['Turnaround_Time_hours'].mean():.1f} jam")
    
    st.divider()
    
    df_filtered = df.copy()
    if ship_filter != "Semua":
        df_filtered = df_filtered[df_filtered["Ship_Type"] == ship_filter]
    if route_filter != "Semua":
        df_filtered = df_filtered[df_filtered["Route_Type"] == route_filter]
        
    st.caption(f"Menampilkan {len(df_filtered):,} rekor kapal aktif berdasarkan filter")
    st.dataframe(df_filtered, use_container_width=True, height=350)

# TAB 2 — KURVA KEANGGOTAAN FUZZY
with tab2:
    st.markdown("### Visualisasi Fungsi Keanggotaan")
    st.caption("Kurva keanggotaan variabel linguistik (Rendah, Sedang, Tinggi) untuk seluruh kriteria penilaian fuzifikasi.")

    MF_COLORS = {"Low": "#2a9d8f", "Medium": "#f7a5b0", "High": "#e8637a"}

    # Visualisasi kurva menggunakan skfuzzy.trimf untuk ke-5 kriteria
    for key in CRIT_KEYS:
        label = CRITERIA[key]["label"]
        x = np.linspace(df[key].min(), df[key].max(), 200)
        mid = np.median(df[key])

        mfs = {
            "Rendah": fuzz.trimf(x, [x.min(), x.min(), mid]),
            "Sedang": fuzz.trimf(x, [x.min(), mid, x.max()]),
            "Tinggi": fuzz.trimf(x, [mid, x.max(), x.max()]),
        }

        fig, ax = plt.subplots(figsize=(8, 2.5))
        for name, mf in mfs.items():
            c = MF_COLORS["Low"] if name == "Rendah" else (MF_COLORS["Medium"] if name == "Sedang" else MF_COLORS["High"])
            ax.plot(x, mf, color=c, linewidth=2, label=name)
            ax.fill_between(x, mf, alpha=0.1, color=c)

        ax.set_title(f"Variabel Input: {label}", color="#f0f6ff", fontsize=10, pad=8)
        ax.set_yticks([0, 0.5, 1.0])
        ax.set_ylim(-0.05, 1.1)
        ax.legend(loc="upper right", framealpha=0.2, labelcolor="#f0f6ff", fontsize=8, facecolor="#060b19")
        ax.grid(alpha=0.2)
        ax.spines[:].set_visible(False)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.divider()
    st.markdown("**Variabel Output: Indeks Skor Prioritas Pelayanan**")
    x_out = np.linspace(0, 100, 200)
    mfs_out = {
        "Rendah": fuzz.trimf(x_out, [0, 0, 50]),
        "Sedang": fuzz.trimf(x_out, [0, 50, 100]),
        "Tinggi": fuzz.trimf(x_out, [50, 100, 100]),
    }
    
    fig3, ax3 = plt.subplots(figsize=(8, 2.5))
    for name, mf in mfs_out.items():
        c = MF_COLORS["Low"] if name == "Rendah" else (MF_COLORS["Medium"] if name == "Sedang" else MF_COLORS["High"])
        ax3.plot(x_out, mf, color=c, linewidth=2, label=name)
        ax3.fill_between(x_out, mf, alpha=0.1, color=c)
        
    ax3.set_title("Output: Tingkat Kelayakan Sandar Kapal", color="#f0f6ff", fontsize=10, pad=8)
    ax3.set_yticks([0, 0.5, 1.0])
    ax3.set_ylim(-0.05, 1.1)
    ax3.legend(loc="upper right", framealpha=0.2, labelcolor="#f0f6ff", fontsize=8, facecolor="#060b19")
    ax3.grid(alpha=0.2)
    ax3.spines[:].set_visible(False)
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close()

# TAB 3 — BASIS ATURAN
with tab3:
    st.markdown("### Basis Aturan Keputusan Fuzzy")
    st.caption("Kombinasi keputusan logis dari interaksi 5 matriks parameter pelayaran.")

    LEVELS = ["Rendah", "Sedang", "Tinggi"]
    SCORE_MAP = {"Rendah": 0, "Sedang": 1, "Tinggi": 2}
    OUT_MAP   = lambda s: "Tinggi" if s >= 3 else ("Rendah" if s <= -1 else "Sedang")

    rules = []
    for spd in LEVELS:
        for cg in LEVELS:
            for rv in LEVELS:
                for cs in LEVELS:
                    for tr in LEVELS:
                        score = (SCORE_MAP[spd] + SCORE_MAP[cg] + SCORE_MAP[rv]
                                 - SCORE_MAP[cs] - SCORE_MAP[tr])
                        out = OUT_MAP(score)
                        rules.append({
                            "JIKA Kecepatan":  spd,
                            "DAN Kargo":       cg,
                            "DAN Revenue":     rv,
                            "DAN Biaya Op.":   cs,
                            "DAN Waktu Sandar": tr,
                            "MAKA Prioritas":  out
                        })

    rule_df = pd.DataFrame(rules)
    out_counts = rule_df["MAKA Prioritas"].value_counts()

    LOCAL_COLORS = {"Rendah": "#e8637a", "Sedang": "#f7a5b0", "Tinggi": "#2a9d8f"}

    col_r1, col_r2 = st.columns([1.6, 1])

    with col_r2:
        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        
        # Mapping warna pie chart
        pie_colors = [LOCAL_COLORS.get(l, "#84d8c4") for l in out_counts.index]
        
        wedges, texts, autotexts = ax.pie(
            out_counts.values, 
            labels=out_counts.index,
            colors=pie_colors, 
            autopct="%1.1f%%", 
            pctdistance=0.7, 
            startangle=140,
            wedgeprops={"edgecolor": "#060b19", "linewidth": 2, "alpha": 0.9}
        )
        for t in texts: 
            t.set_color("#f0f6ff")
        for at in autotexts:
            at.set_color("#060b19")
            at.set_fontweight("bold")
            
        ax.set_title("Distribusi Penetapan\nPrioritas Pelayanan", color="#f0f6ff", fontsize=11, pad=10)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_r1:
        def color_output(val):
            color_map = {
                "Tinggi": "background-color:#1a4a30; color:#84d8c4",
                "Sedang": "background-color:#3a2a10; color:#f4c542",
                "Rendah": "background-color:#3a1020; color:#f7a5b0",
            }
            return color_map.get(val, "")

        styled = rule_df.style.map(color_output, subset=["MAKA Prioritas"])
        st.dataframe(styled, height=420, use_container_width=True)

# TAB 4 — HASIL REKOMENDASI KAPAL TERBAIK
with tab4:
    st.markdown("### Hasil Perankingan Kapal Terbaik")

    if not is_weight_valid:
        st.warning("Perhitungan Terkunci. Silakan sesuaikan jumlah kriteria bobot di sidebar agar bernilai pas 1.00.")
    elif not run:
        st.markdown("""
        <div style="background:rgba(6,11,25,0.6); border:1px dashed rgba(255,255,255,0.2); border-radius:14px; padding:40px; text-align:center; color:#8899bb;">
            <div style="font-size:2.5rem; margin-bottom:12px;">⚓</div>
            <div style="font-size:1rem;">Kriteria Bobot Valid Klik tombol<br>
            <b style="color:#84d8c4;">Jalankan Seleksi Fuzzy</b> di sidebar untuk memproses perangkingan armada.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        weights = np.array([w_speed, w_cargo, w_rev, w_cost, w_turn])
        weights /= weights.sum()

        if df_filtered.empty:
            st.error("Data kosong untuk kombinasi filter ini.")
        else:
            def normalize_col(series, is_benefit):
                mn, mx = series.min(), series.max()
                if mx == mn: return pd.Series(np.ones(len(series)), index=series.index)
                return (series - mn) / (mx - mn) if is_benefit else (mx - series) / (mx - mn)

            norm_matrix = {}
            norm_matrix["Speed_Over_Ground_knots"] = normalize_col(df_filtered["Speed_Over_Ground_knots"], CRITERIA["Speed_Over_Ground_knots"]["benefit"])
            norm_matrix["Cargo_Weight_tons"] = normalize_col(df_filtered["Cargo_Weight_tons"], CRITERIA["Cargo_Weight_tons"]["benefit"])
            norm_matrix["Revenue_per_Voyage_USD"] = normalize_col(df_filtered["Revenue_per_Voyage_USD"], CRITERIA["Revenue_per_Voyage_USD"]["benefit"])
            norm_matrix["Operational_Cost_USD"] = normalize_col(df_filtered["Operational_Cost_USD"], CRITERIA["Operational_Cost_USD"]["benefit"])
            norm_matrix["Turnaround_Time_hours"] = normalize_col(df_filtered["Turnaround_Time_hours"], CRITERIA["Turnaround_Time_hours"]["benefit"])

            final_scores = (weights[0] * norm_matrix["Speed_Over_Ground_knots"] +
                            weights[1] * norm_matrix["Cargo_Weight_tons"] +
                            weights[2] * norm_matrix["Revenue_per_Voyage_USD"] +
                            weights[3] * norm_matrix["Operational_Cost_USD"] +
                            weights[4] * norm_matrix["Turnaround_Time_hours"]) * 100

            result_df = df_filtered.copy()
            result_df["Fuzzy_Score"] = final_scores.values
            result_df = result_df.sort_values("Fuzzy_Score", ascending=False).reset_index(drop=True)
            result_df.insert(0, "Rank", range(1, len(result_df) + 1))

            top_vessel = result_df.iloc[0]

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(6,11,25,0.85), rgba(42,157,143,0.3)); border: 1px solid rgba(255,255,255,0.2); border-radius: 16px; padding: 20px 28px; margin-bottom: 20px;">
                <p style="color:#84d8c4; font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; margin:0 0 4px;">Rekomendasi Utama: Kapal dengan Kelayakan Sandar Terbaik (Rank #1)</p>
                <h2 style="margin:0 0 6px; font-size:1.8rem; background:linear-gradient(90deg, #f0f6ff, #84d8c4); -webkit-background-clip:text; -webkit-text-fill-color: transparent;">
                    {top_vessel['Ship_Type']} ({top_vessel.get('Route_Type','–')})
                </h2>
                <p style="color:#ff8fa3; font-size:0.9rem; margin:0;">
                    Indeks Kelayakan Fuzzy: <b>{top_vessel['Fuzzy_Score']:.2f} / 100</b> &nbsp;|&nbsp; 
                    Muatan: {top_vessel['Cargo_Weight_tons']:.1f} ton &nbsp;|&nbsp; 
                    Waktu Sandar: {top_vessel['Turnaround_Time_hours']:.1f} jam
                </p>
            </div>
            """, unsafe_allow_html=True)

            col_g1, col_g2 = st.columns([1.3, 1])
            with col_g1:
                st.markdown(f"**Tabel Top {min(int(top_n), len(result_df))} Urutan Hasil Seleksi**")
                cols_display = ["Rank", "Ship_Type", "Route_Type", "Speed_Over_Ground_knots", "Cargo_Weight_tons", "Turnaround_Time_hours", "Fuzzy_Score"]
                st.dataframe(result_df.head(int(top_n))[cols_display], use_container_width=True, height=380)

            with col_g2:
                st.markdown("**Grafik Komparasi Skor Kelayakan**")
                top_data = result_df.head(int(top_n))
                fig4, ax4 = plt.subplots(figsize=(5, max(4, len(top_data) * 0.35)))
                
                scores_plot = top_data["Fuzzy_Score"].values[::-1]
                labels_plot = (top_data["Ship_Type"] + " #" + top_data["Rank"].astype(str)).values[::-1]
                
                bars = ax4.barh(range(len(scores_plot)), scores_plot, color=plt.cm.YlGnBu(np.linspace(0.3, 0.9, len(scores_plot))), edgecolor="none", height=0.6)
                ax4.set_yticks(range(len(labels_plot)))
                ax4.set_yticklabels(labels_plot, fontsize=8)
                ax4.set_xlabel("Fuzzy Score (0-100)", color="#8899bb")
                ax4.grid(axis="x", alpha=0.2)
                ax4.spines[:].set_visible(False)
                fig4.tight_layout()
                st.pyplot(fig4)
                plt.close()

# TAB 5 — TIM PENGEMBANG
with tab5:
    st.markdown("### Profil Analis Kelompok")
    col_d1, col_d2 = st.columns(2)

    def draw_profile(col, name, nim, img_url):
        col.markdown(f"""
        <div style="background: rgba(6,11,25,0.6); border: 1px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 28px 24px; text-align: center;">
            <div style="width:100px; height:100px; border-radius:50%; overflow:hidden; border: 3px solid #84d8c4; box-shadow: 0 0 10px rgba(132,216,196,0.5); margin:0 auto 14px; display:flex; align-items:center; justify-content:center;">
                <img src="{img_url}" style="width:100%; height:100%; object-fit:cover;" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png'">
            </div>
            <h3 style="margin:0 0 6px; background:linear-gradient(90deg,#84d8c4,#ff8fa3); -webkit-background-clip:text; -webkit-text-fill-color: transparent; font-size:1.1rem;">{name}</h3>
            <p style="color:#f4c542; font-size:0.82rem; margin:0 0 4px; font-weight:600;">{nim}</p>
            <p style="color:#8899bb; font-size:0.78rem; margin:0;">Program Studi Informatika</p>
            <p style="color:#8899bb; font-size:0.78rem; margin:0;">UPN "Veteran" Yogyakarta</p>
        </div>
        """, unsafe_allow_html=True)

    URL_FOTO_KURNIA  = "https://raw.githubusercontent.com/yayaaaawww/Projek-Prak-SCPK/main/WhatsApp%20Image%202026-06-04%20at%2013.09.13.jpeg"
    URL_FOTO_SABRINA = "https://raw.githubusercontent.com/yayaaaawww/Projek-Prak-SCPK/main/WhatsApp%20Image%202026-06-04%20at%2013.04.29.jpeg"

    draw_profile(col_d1, "Kurnia Ardiningrum", "NIM: 123240101", URL_FOTO_KURNIA)
    draw_profile(col_d2, "Sabrina Alya", "NIM: 123240196", URL_FOTO_SABRINA)