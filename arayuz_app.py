"""
OmniPDR – arayuz_app.py
=========================
Ultra-Profesyonel PDR Öğrenci Takip Platformu
Türk Eğitim Sistemi Entegrasyonlu Dashboard

Sekmeler:
  🏠 Ana Dashboard | 🎯 Puan & Sıralama | 🏛️ Üniversite Öneri
  📚 Konu Takibi  | 📅 Çalışma Planı   | 🔁 Tekrar Takibi
  📓 PDR Notları
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import math

# Yerel modüller
from models.ogrenci_sinifi import Ogrenci, DenemeKaydi, HataKaydi, GorusmeNotu
from core.veritabani import OgrenciRepository
from core.analiz_motoru import AnalizMotoru
from core.puan_hesaplama import (
    TYT_DERSLER, AYT_DERSLER, LGS_DERSLER,
    AYT_PUAN_KATSAYILARI,
    net_hesapla_yks, net_hesapla_lgs,
    tyt_puan_hesapla, ayt_puan_hesapla,
    yerlestirme_puani_hesapla, lgs_puan_hesapla,
    tam_puan_hesapla, _siralama_tahmin,
    TYT_SIRALAMA_TABLOSU,
)
from core.yokatlas_verileri import (
    bolum_ara, universite_oner,
    benzersiz_sehirler, benzersiz_bolumler,
    BOLUM_VERILERI,
)
from models.konu_verileri import (
    konu_listesi_getir, tum_dersler,
    TYT_KONULARI, AYT_KONULARI, LGS_KONULARI,
)


# ══════════════════════════════════════════════
# Sayfa Ayarları
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="OmniPDR – Öğrenci Takip Platformu",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ══════════════════════════════════════════════
# CSS – Premium Dark Theme
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root & Typography ───────────────────── */
:root {
    --bg-primary: #0f1117;
    --bg-secondary: #1a1d29;
    --bg-card: #1e2130;
    --bg-hover: #252840;
    --accent-primary: #6C63FF;
    --accent-secondary: #00D2FF;
    --accent-success: #00E676;
    --accent-warning: #FFD600;
    --accent-danger: #FF5252;
    --accent-orange: #FF6D00;
    --text-primary: #E8EAED;
    --text-secondary: #9AA0A6;
    --text-muted: #5F6368;
    --border-color: #2d3250;
    --gradient-1: linear-gradient(135deg, #6C63FF 0%, #00D2FF 100%);
    --gradient-2: linear-gradient(135deg, #FF6D00 0%, #FFD600 100%);
    --gradient-3: linear-gradient(135deg, #00E676 0%, #00D2FF 100%);
    --shadow-card: 0 4px 24px rgba(0,0,0,0.3);
    --shadow-glow: 0 0 20px rgba(108,99,255,0.15);
}
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.stApp {
    background: var(--bg-primary) !important;
}

/* ── Sidebar ───────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #13152a 0%, #1a1d35 100%) !important;
    border-right: 1px solid var(--border-color);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary) !important;
}

/* ── Metric Cards ─────────────────────── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: var(--shadow-card);
    transition: all 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-glow);
    border-color: var(--accent-primary);
}
.metric-value {
    font-size: 2.5rem;
    font-weight: 800;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}
.metric-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Hero Banner ──────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #1a1d40 0%, #2d1f5e 50%, #1a3a5c 100%);
    border-radius: 20px;
    padding: 32px 40px;
    margin-bottom: 24px;
    border: 1px solid rgba(108,99,255,0.3);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(108,99,255,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: #fff;
    margin: 0;
}
.hero-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    margin-top: 8px;
}

/* ── Countdown ────────────────────────── */
.countdown-box {
    background: linear-gradient(135deg, rgba(108,99,255,0.15) 0%, rgba(0,210,255,0.1) 100%);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
}
.countdown-number {
    font-size: 3rem;
    font-weight: 800;
    color: var(--accent-secondary);
}
.countdown-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ── Uni Card ─────────────────────────── */
.uni-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}
.uni-card:hover {
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-glow);
}
.uni-card-title {
    font-weight: 700;
    color: var(--text-primary);
    font-size: 1rem;
}
.uni-card-subtitle {
    color: var(--text-secondary);
    font-size: 0.85rem;
}
.uni-card-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-guvenli { background: rgba(0,230,118,0.15); color: #00E676; }
.badge-dengeli { background: rgba(108,99,255,0.15); color: #6C63FF; }
.badge-sans { background: rgba(255,82,82,0.15); color: #FF5252; }

/* ── Progress bars ────────────────────── */
.konu-progress-bar {
    height: 8px;
    background: var(--bg-hover);
    border-radius: 4px;
    overflow: hidden;
    margin: 4px 0;
}
.konu-progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* ── Tab styling ──────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: var(--text-secondary);
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-primary) !important;
    color: white !important;
}

/* ── Buttons ──────────────────────────── */
.stButton > button {
    background: var(--gradient-1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 8px 24px !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.4) !important;
}

/* ── Inputs ───────────────────────────── */
input, .stSelectbox, .stNumberInput, textarea {
    border-radius: 10px !important;
}

/* ── Hide Streamlit defaults ──────────── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Plotly dark theme override ───────── */
.js-plotly-plot .plotly .modebar { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# Session State ve Repository
# ══════════════════════════════════════════════
repo = OgrenciRepository()


def _state(key, default=None):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


_state("secili_ogrenci_id", None)
_state("aktif_sekme", 0)


def secili_ogrenci():
    oid = st.session_state.get("secili_ogrenci_id")
    if oid:
        return repo.bul(oid)
    return None


# ══════════════════════════════════════════════
# Sınav Geri Sayımı
# ══════════════════════════════════════════════
YKS_2025 = datetime(2025, 6, 14)
LGS_2025 = datetime(2025, 6, 8)
# 2026 tarihleri (tahmini)
YKS_TARIH = datetime(2026, 6, 13)
LGS_TARIH = datetime(2026, 6, 7)


def geri_sayim_goster(sinav_turu="YKS"):
    hedef = YKS_TARIH if sinav_turu == "YKS" else LGS_TARIH
    bugun = datetime.now()
    fark = hedef - bugun

    if fark.days < 0:
        st.info(f"📅 {sinav_turu} 2026 tamamlandı!")
        return

    gun = fark.days
    saat = fark.seconds // 3600
    dakika = (fark.seconds % 3600) // 60

    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"""
        <div class="countdown-box">
            <div class="countdown-number">{gun}</div>
            <div class="countdown-label">Gün</div>
        </div>""", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class="countdown-box">
            <div class="countdown-number">{saat}</div>
            <div class="countdown-label">Saat</div>
        </div>""", unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class="countdown-box">
            <div class="countdown-number">{dakika}</div>
            <div class="countdown-label">Dakika</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# Yardımcı Fonksiyonlar
# ══════════════════════════════════════════════
def metric_card(etiket, deger, renk="var(--gradient-1)"):
    return f"""
    <div class="metric-card">
        <div class="metric-value" style="background:{renk};-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{deger}</div>
        <div class="metric-label">{etiket}</div>
    </div>"""


def format_siralama(s):
    if s is None:
        return "—"
    if s >= 1_000_000:
        return f"{s/1_000_000:.1f}M"
    if s >= 1_000:
        return f"{s/1_000:,.0f}K".replace(",", ".")
    return str(s)


# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧠 OmniPDR")
    st.markdown("*Profesyonel PDR Platformu*")
    st.markdown("---")

    # Öğrenci seçimi veya ekleme
    ogrenciler = repo.tum_ogrenciler()
    isimler = [o.ad for o in ogrenciler]

    if isimler:
        secim = st.selectbox("👤 Öğrenci Seç", isimler, key="sb_ogrenci")
        for o in ogrenciler:
            if o.ad == secim:
                st.session_state["secili_ogrenci_id"] = o.ogrenci_id
                break

    st.markdown("---")

    with st.expander("➕ Yeni Öğrenci Ekle", expanded=not bool(isimler)):
        yeni_ad = st.text_input("Ad Soyad", key="yeni_ad")
        yeni_sinav = st.selectbox("Sınav Türü", ["YKS", "LGS"], key="yeni_sinav")

        if yeni_sinav == "YKS":
            yeni_puan_turu = st.selectbox("Puan Türü", ["SAY", "EA", "SOZ"], key="yeni_pt")
        else:
            yeni_puan_turu = "LGS"

        yeni_bolum = st.text_input("Hedef Bölüm", key="yeni_bolum")
        yeni_obp = st.number_input("OBP (Diploma Notu × 5)", 0.0, 500.0, 350.0, key="yeni_obp")
        yeni_hedef_sir = st.number_input("Hedef Sıralama", 1, 3_000_000, 50000, key="yeni_sir")

        if st.button("✨ Öğrenci Oluştur", use_container_width=True):
            if yeni_ad.strip():
                yeni = Ogrenci(
                    ad=yeni_ad.strip(),
                    hedef_bolum=yeni_bolum.strip() or "Belirlenmedi",
                    sinav_turu=yeni_sinav,
                    obp=yeni_obp,
                    hedef_puan_turu=yeni_puan_turu,
                    hedef_siralama=yeni_hedef_sir,
                )
                repo.ekle(yeni)
                st.session_state["secili_ogrenci_id"] = yeni.ogrenci_id
                st.success(f"✅ {yeni_ad} eklendi!")
                st.rerun()

    st.markdown("---")
    st.caption("v2.0 • Ultra-Profesyonel")


# ══════════════════════════════════════════════
# ANA İÇERİK
# ══════════════════════════════════════════════
ogr = secili_ogrenci()

if not ogr:
    st.markdown("""
    <div class="hero-banner" style="text-align:center; padding:60px;">
        <h1 style="font-size:3rem; margin:0;">🧠 OmniPDR</h1>
        <p style="font-size:1.3rem; color:#9AA0A6; margin-top:12px;">
            Profesyonel PDR Öğrenci Takip & Analiz Platformu
        </p>
        <p style="font-size:1rem; color:#5F6368; margin-top:8px;">
            Türk Eğitim Sistemi • YKS/LGS • YÖK Atlas Entegrasyonu
        </p>
        <hr style="border-color: rgba(108,99,255,0.2); margin: 24px 0;">
        <p style="color:#9AA0A6;">👈 Sol menüden öğrenci ekleyerek başlayın</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Analiz motoru ──
analiz = AnalizMotoru(ogr)

# ── Banner ──
st.markdown(f"""
<div class="hero-banner">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
        <div>
            <div class="hero-title">👋 {ogr.ad}</div>
            <div class="hero-subtitle">
                {ogr.sinav_turu} • {ogr.hedef_puan_turu if ogr.sinav_turu == 'YKS' else 'LGS'} •
                Hedef: {ogr.hedef_bolum} •
                Hedef Sıra: {format_siralama(ogr.hedef_siralama)}
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px;">
                {ogr.sinav_turu} 2026'YA KALAN
            </div>
            <div style="font-size:2rem; font-weight:800; color:var(--accent-secondary);">
                {(YKS_TARIH - datetime.now()).days if ogr.sinav_turu == 'YKS' else (LGS_TARIH - datetime.now()).days} gün
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# SEKMELER
# ══════════════════════════════════════════════
sekmeler = st.tabs([
    "🏠 Dashboard",
    "🎯 Puan & Sıralama",
    "🏛️ Üniversite Öneri",
    "📚 Konu Takibi",
    "📝 Deneme Ekle",
    "🔁 Tekrar Takibi",
    "📓 PDR Notları",
])


# ──────────────────────────────────────────────
# SEKME 1: ANA DASHBOARD
# ──────────────────────────────────────────────
with sekmeler[0]:
    # Geri sayım
    geri_sayim_goster(ogr.sinav_turu)
    st.markdown("<br>", unsafe_allow_html=True)

    # Üst metrikler
    deneme_sayisi = len(ogr.deneme_kayitlari)
    if deneme_sayisi > 0:
        son_deneme = ogr.deneme_kayitlari[-1]
        son_toplam_net = sum(son_deneme.ders_netleri.values())
        ortalama_net = sum(
            sum(d.ders_netleri.values()) for d in ogr.deneme_kayitlari
        ) / deneme_sayisi

        # Trend hesapla
        if deneme_sayisi >= 2:
            onceki_net = sum(ogr.deneme_kayitlari[-2].ders_netleri.values())
            trend = son_toplam_net - onceki_net
            trend_str = f"{'↑' if trend > 0 else '↓'} {abs(trend):.1f}"
        else:
            trend_str = "—"

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(metric_card("Son Deneme Net", f"{son_toplam_net:.1f}"), unsafe_allow_html=True)
        with mc2:
            st.markdown(metric_card("Ortalama Net", f"{ortalama_net:.1f}",
                                     "linear-gradient(135deg, #00D2FF, #00E676)"), unsafe_allow_html=True)
        with mc3:
            st.markdown(metric_card("Deneme Sayısı", str(deneme_sayisi),
                                     "linear-gradient(135deg, #FF6D00, #FFD600)"), unsafe_allow_html=True)
        with mc4:
            st.markdown(metric_card("Trend", trend_str,
                                     "linear-gradient(135deg, #00E676, #6C63FF)"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Net Gelişim Grafiği
        col_g1, col_g2 = st.columns([3, 2])
        with col_g1:
            st.subheader("📈 Net Gelişim Grafiği")
            df_data = []
            for d in ogr.deneme_kayitlari:
                for ders, net in d.ders_netleri.items():
                    df_data.append({
                        "Tarih": d.tarih.isoformat(),
                        "Ders": ders,
                        "Net": net,
                    })
            if df_data:
                df = pd.DataFrame(df_data)
                fig = px.line(
                    df, x="Tarih", y="Net", color="Ders",
                    markers=True,
                    template="plotly_dark",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                )
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#9AA0A6",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3),
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=350,
                )
                st.plotly_chart(fig, use_container_width=True)

        with col_g2:
            st.subheader("📊 Son Deneme Dağılımı")
            if son_deneme.ders_netleri:
                df_pie = pd.DataFrame([
                    {"Ders": k, "Net": v} for k, v in son_deneme.ders_netleri.items()
                ])
                fig_pie = px.bar(
                    df_pie, x="Net", y="Ders", orientation="h",
                    template="plotly_dark",
                    color="Net",
                    color_continuous_scale="Viridis",
                )
                fig_pie.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#9AA0A6",
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=350,
                    showlegend=False,
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        # Detaylı analiz
        rapor = analiz.genel_rapor()
        if rapor:
            st.markdown("<br>", unsafe_allow_html=True)
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                st.markdown("#### 💪 Güçlü Dersler")
                for d in (rapor.guclu_dersler or []):
                    st.success(f"✅ {d}")
            with col_a2:
                st.markdown("#### ⚠️ Zayıf Dersler")
                for d in (rapor.zayif_dersler or []):
                    st.warning(f"📉 {d}")
            with col_a3:
                st.markdown("#### 🔥 Durum")
                yanma = analiz.zimmerman_oz_duzenleme()
                if yanma:
                    if yanma.get("risk_seviyesi") == "Yüksek":
                        st.error(f"🚨 Tükenmişlik Riski: {yanma.get('risk_seviyesi')}")
                    elif yanma.get("risk_seviyesi") == "Orta":
                        st.warning(f"⚡ Tükenmişlik Riski: {yanma.get('risk_seviyesi')}")
                    else:
                        st.info(f"✨ Tükenmişlik Riski: {yanma.get('risk_seviyesi', 'Düşük')}")
                zpd = analiz.vygotsky_zpd()
                if zpd:
                    st.info(f"📐 ZPD Bölgesi: {zpd.get('bolge', '?')}")

    else:
        st.info("📝 Henüz deneme kaydı yok. **Deneme Ekle** sekmesinden ilk denemenizi girin!")


# ──────────────────────────────────────────────
# SEKME 2: PUAN & SIRALAMA
# ──────────────────────────────────────────────
with sekmeler[1]:
    st.subheader("🎯 Net → Puan Dönüşümü & Sıralama Tahmini")

    if ogr.sinav_turu == "YKS":
        tab_tyt, tab_ayt, tab_sonuc = st.tabs(["TYT Netleri", "AYT Netleri", "📊 Sonuç"])

        with tab_tyt:
            st.markdown("**TYT – Temel Yeterlilik Testi** (120 soru)")
            tyt_cols = st.columns(4)
            tyt_netleri = {}
            for i, (ders, bilgi) in enumerate(TYT_DERSLER.items()):
                with tyt_cols[i % 4]:
                    tyt_netleri[ders] = st.number_input(
                        f"{ders} ({bilgi['soru_sayisi']} soru)",
                        0.0, float(bilgi["soru_sayisi"]), 0.0,
                        step=0.5, key=f"tyt_{ders}"
                    )

        with tab_ayt:
            puan_turu = ogr.hedef_puan_turu
            st.markdown(f"**AYT – Alan Yeterlilik Testi** (Puan Türü: **{puan_turu}**)")
            katsayilar = AYT_PUAN_KATSAYILARI.get(puan_turu, {})
            aktif_dersler = {d: b for d, b in AYT_DERSLER.items() if katsayilar.get(d, 0) > 0}

            ayt_cols = st.columns(min(4, len(aktif_dersler)))
            ayt_netleri = {}
            for i, (ders, bilgi) in enumerate(aktif_dersler.items()):
                with ayt_cols[i % len(ayt_cols)]:
                    ayt_netleri[ders] = st.number_input(
                        f"{ders} ({bilgi['soru_sayisi']} soru)",
                        0.0, float(bilgi["soru_sayisi"]), 0.0,
                        step=0.5, key=f"ayt_{ders}"
                    )

        with tab_sonuc:
            if st.button("🧮 Puanı Hesapla", use_container_width=True, key="btn_puan"):
                sonuc = tam_puan_hesapla(tyt_netleri, ayt_netleri, puan_turu, ogr.obp)
                tyt_p = sonuc.detay.get("TYT Puanı", 0)

                col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                with col_r1:
                    st.markdown(metric_card("TYT Puanı", f"{tyt_p:.1f}"), unsafe_allow_html=True)
                with col_r2:
                    st.markdown(metric_card("AYT Puanı", f"{sonuc.ham_puan:.1f}",
                                             "linear-gradient(135deg, #00D2FF, #00E676)"), unsafe_allow_html=True)
                with col_r3:
                    st.markdown(metric_card("Yerleştirme", f"{sonuc.yerlestirme_puani:.1f}",
                                             "linear-gradient(135deg, #FF6D00, #FFD600)"), unsafe_allow_html=True)
                with col_r4:
                    st.markdown(metric_card("Tahmini Sıra", format_siralama(sonuc.tahmini_siralama),
                                             "linear-gradient(135deg, #FF5252, #FF6D00)"), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 📋 Detaylar")
                for k, v in sonuc.detay.items():
                    st.markdown(f"- **{k}:** {v}")

                # Hedef karşılaştırma
                if ogr.hedef_siralama:
                    st.markdown("---")
                    if sonuc.tahmini_siralama <= ogr.hedef_siralama:
                        st.success(f"🎉 Hedefinize ulaşıyorsunuz! (Hedef: {format_siralama(ogr.hedef_siralama)})")
                    else:
                        fark = sonuc.tahmini_siralama - ogr.hedef_siralama
                        st.warning(f"📊 Hedefe {format_siralama(fark)} sıra daha var (Hedef: {format_siralama(ogr.hedef_siralama)})")

    else:
        # LGS
        st.markdown("**LGS – Liseye Geçiş Sınavı** (90 soru)")
        lgs_cols = st.columns(3)
        lgs_netleri = {}
        for i, (ders, bilgi) in enumerate(LGS_DERSLER.items()):
            with lgs_cols[i % 3]:
                lgs_netleri[ders] = st.number_input(
                    f"{ders} ({bilgi['soru_sayisi']} soru)",
                    0.0, float(bilgi["soru_sayisi"]), 0.0,
                    step=0.5, key=f"lgs_{ders}"
                )

        if st.button("🧮 LGS Puanı Hesapla", use_container_width=True, key="btn_lgs"):
            sonuc = lgs_puan_hesapla(lgs_netleri)
            col_l1, col_l2, col_l3 = st.columns(3)
            with col_l1:
                st.markdown(metric_card("LGS Puanı", f"{sonuc.puan:.1f}"), unsafe_allow_html=True)
            with col_l2:
                st.markdown(metric_card("Tahmini Sıra", format_siralama(sonuc.tahmini_siralama),
                                         "linear-gradient(135deg, #00D2FF, #00E676)"), unsafe_allow_html=True)
            with col_l3:
                st.markdown(metric_card("Yüzdelik", f"%{sonuc.tahmini_yuzdelik:.1f}",
                                         "linear-gradient(135deg, #FF6D00, #FFD600)"), unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SEKME 3: ÜNİVERSİTE ÖNERİ
# ──────────────────────────────────────────────
with sekmeler[2]:
    st.subheader("🏛️ Üniversite & Bölüm Öneri Sistemi")

    if ogr.sinav_turu == "LGS":
        st.info("🎓 Bu özellik YKS öğrencileri için aktiftir. LGS lise tercih rehberi yakında!")
    else:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filtre_puan = st.number_input("Tahmini Puanınız", 100.0, 500.0, 350.0, key="filtre_puan")
        with col_f2:
            filtre_pt = st.selectbox("Puan Türü", ["SAY", "EA", "SOZ"], key="filtre_pt",
                                      index=["SAY", "EA", "SOZ"].index(ogr.hedef_puan_turu) if ogr.hedef_puan_turu in ["SAY", "EA", "SOZ"] else 0)
        with col_f3:
            filtre_sehir = st.selectbox("Şehir (Opsiyonel)", ["Tümü"] + benzersiz_sehirler(), key="filtre_sehir")

        oneriler = universite_oner(filtre_puan, filtre_pt)

        # Güvenli
        st.markdown("### 🟢 Güvenli Tercihler")
        st.caption("Bu puanla rahatlıkla yerleşebileceğiniz bölümler")
        for b in oneriler["guvenli"]:
            if filtre_sehir != "Tümü" and b.sehir != filtre_sehir:
                continue
            st.markdown(f"""
            <div class="uni-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="uni-card-title">{b.bolum}</div>
                        <div class="uni-card-subtitle">{b.universite} • {b.sehir} • {b.tur}</div>
                    </div>
                    <div style="text-align:right;">
                        <div><span class="uni-card-badge badge-guvenli">{b.puan_turu}</span></div>
                        <div style="color:var(--accent-success); font-weight:700;">{b.taban_puan:.1f} puan</div>
                        <div style="color:var(--text-muted); font-size:0.8rem;">Sıra: {format_siralama(b.siralama)}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Dengeli
        st.markdown("### 🟡 Dengeli Tercihler")
        st.caption("Puanınıza yakın, iyi şansınız olan bölümler")
        for b in oneriler["dengeli"]:
            if filtre_sehir != "Tümü" and b.sehir != filtre_sehir:
                continue
            st.markdown(f"""
            <div class="uni-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="uni-card-title">{b.bolum}</div>
                        <div class="uni-card-subtitle">{b.universite} • {b.sehir} • {b.tur}</div>
                    </div>
                    <div style="text-align:right;">
                        <div><span class="uni-card-badge badge-dengeli">{b.puan_turu}</span></div>
                        <div style="color:var(--accent-primary); font-weight:700;">{b.taban_puan:.1f} puan</div>
                        <div style="color:var(--text-muted); font-size:0.8rem;">Sıra: {format_siralama(b.siralama)}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Şans
        st.markdown("### 🔴 Şans Tercihleri")
        st.caption("Biraz risk içeren ama şansınızı deneyebileceğiniz bölümler")
        for b in oneriler["sans"]:
            if filtre_sehir != "Tümü" and b.sehir != filtre_sehir:
                continue
            st.markdown(f"""
            <div class="uni-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="uni-card-title">{b.bolum}</div>
                        <div class="uni-card-subtitle">{b.universite} • {b.sehir} • {b.tur}</div>
                    </div>
                    <div style="text-align:right;">
                        <div><span class="uni-card-badge badge-sans">{b.puan_turu}</span></div>
                        <div style="color:var(--accent-danger); font-weight:700;">{b.taban_puan:.1f} puan</div>
                        <div style="color:var(--text-muted); font-size:0.8rem;">Sıra: {format_siralama(b.siralama)}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Bölüm arama
        st.markdown("---")
        st.subheader("🔍 Bölüm Arama")
        arama = st.text_input("Bölüm adı yazın...", key="bolum_arama")
        if arama:
            bulunanlar = bolum_ara(bolum_adi=arama, puan_turu=filtre_pt)
            if bulunanlar:
                df_b = pd.DataFrame([{
                    "Üniversite": b.universite,
                    "Bölüm": b.bolum,
                    "Şehir": b.sehir,
                    "Taban Puan": b.taban_puan,
                    "Sıralama": b.siralama,
                    "Kontenjan": b.kontenjan,
                    "Tür": b.tur,
                } for b in bulunanlar])
                st.dataframe(df_b, use_container_width=True, hide_index=True)
            else:
                st.warning("Bu kriterlere uygun bölüm bulunamadı.")


# ──────────────────────────────────────────────
# SEKME 4: KONU TAKİBİ
# ──────────────────────────────────────────────
with sekmeler[3]:
    st.subheader("📚 Konu Bazlı İlerleme Takibi")

    if ogr.sinav_turu == "LGS":
        konular_dict = LGS_KONULARI
    else:
        konu_tab = st.radio("Sınav Bölümü", ["TYT", "AYT"], horizontal=True, key="konu_sinav")
        konular_dict = TYT_KONULARI if konu_tab == "TYT" else AYT_KONULARI

    # Konu ilerlemelerini göster ve güncelle
    for ders, konular in konular_dict.items():
        with st.expander(f"📖 {ders} ({len(konular)} konu)", expanded=False):
            tamamlanan = 0
            for konu in konular:
                ders_key = ders
                mevcut = ogr.konu_ilerlemeleri.get(ders_key, {}).get(konu, 0)
                yeni = st.slider(
                    konu, 0, 100, mevcut,
                    key=f"konu_{ders_key}_{konu}",
                    format="%d%%",
                )
                if yeni != mevcut:
                    if ders_key not in ogr.konu_ilerlemeleri:
                        ogr.konu_ilerlemeleri[ders_key] = {}
                    ogr.konu_ilerlemeleri[ders_key][konu] = yeni
                    repo.guncelle(ogr)

                if yeni >= 80:
                    tamamlanan += 1

                # Renkli progress bar
                renk = "#00E676" if yeni >= 80 else "#FFD600" if yeni >= 40 else "#FF5252"
                st.markdown(f"""
                <div class="konu-progress-bar">
                    <div class="konu-progress-fill" style="width:{yeni}%; background:{renk};"></div>
                </div>""", unsafe_allow_html=True)

            yuzde = (tamamlanan / len(konular) * 100) if konular else 0
            st.caption(f"✅ {tamamlanan}/{len(konular)} konu tamamlandı (%{yuzde:.0f})")


# ──────────────────────────────────────────────
# SEKME 5: DENEME EKLE
# ──────────────────────────────────────────────
with sekmeler[4]:
    st.subheader("📝 Yeni Deneme Sınavı Kaydı")

    deneme_tarih = st.date_input("Tarih", date.today(), key="deneme_tarih")
    deneme_ad = st.text_input("Deneme Adı (opsiyonel)", placeholder="Örn: TYT-5 Genel", key="deneme_ad")

    st.markdown("#### Ders Netleri")

    if ogr.sinav_turu == "YKS":
        deneme_tab = st.radio("Sınav Bölümü", ["TYT", "AYT"], horizontal=True, key="deneme_bolum")
        if deneme_tab == "TYT":
            dersler = list(TYT_DERSLER.keys())
            soru_sayilari = {d: b["soru_sayisi"] for d, b in TYT_DERSLER.items()}
        else:
            katsayilar = AYT_PUAN_KATSAYILARI.get(ogr.hedef_puan_turu, {})
            dersler = [d for d, k in katsayilar.items() if k > 0]
            soru_sayilari = {d: AYT_DERSLER[d]["soru_sayisi"] for d in dersler if d in AYT_DERSLER}
    else:
        dersler = list(LGS_DERSLER.keys())
        soru_sayilari = {d: b["soru_sayisi"] for d, b in LGS_DERSLER.items()}

    ders_netleri = {}
    cols_dn = st.columns(min(4, len(dersler)))
    for i, ders in enumerate(dersler):
        with cols_dn[i % len(cols_dn)]:
            maks = float(soru_sayilari.get(ders, 40))
            ders_netleri[ders] = st.number_input(
                f"{ders} (max {int(maks)})", 0.0, maks, 0.0,
                step=0.5, key=f"dn_{ders}"
            )

    if st.button("💾 Deneme Kaydet", use_container_width=True, key="btn_deneme_kaydet"):
        # Sıfır olmayan dersleri filtrele
        netleri_filtre = {d: n for d, n in ders_netleri.items() if n > 0}
        if netleri_filtre:
            kayit = DenemeKaydi(
                tarih=deneme_tarih,
                ders_netleri=netleri_filtre,
                deneme_adi=deneme_ad or None,
            )
            ogr.deneme_ekle(kayit)
            repo.guncelle(ogr)
            st.success(f"✅ Deneme kaydedildi! Toplam net: {sum(netleri_filtre.values()):.1f}")
            st.rerun()
        else:
            st.error("⚠️ En az bir derse net girmelisiniz!")

    # Geçmiş denemeler
    if ogr.deneme_kayitlari:
        st.markdown("---")
        st.markdown("#### 📋 Geçmiş Denemeler")
        gecmis_data = []
        for d in reversed(ogr.deneme_kayitlari):
            toplam = sum(d.ders_netleri.values())
            gecmis_data.append({
                "Tarih": d.tarih.isoformat(),
                "Ad": d.deneme_adi or "—",
                "Toplam Net": f"{toplam:.1f}",
                **{k: f"{v:.1f}" for k, v in d.ders_netleri.items()},
            })
        st.dataframe(pd.DataFrame(gecmis_data), use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────
# SEKME 6: TEKRAR TAKİBİ (Ebbinghaus)
# ──────────────────────────────────────────────
with sekmeler[5]:
    st.subheader("🔁 Ebbinghaus Aralıklı Tekrar Takibi")

    col_h1, col_h2 = st.columns([1, 2])
    with col_h1:
        st.markdown("#### ➕ Yeni Hata Kaydı")
        hata_ders = st.text_input("Ders", key="hata_ders")
        hata_konu = st.text_input("Konu / Soru", key="hata_konu")
        hata_aciklama = st.text_area("Açıklama", key="hata_aciklama", height=100)

        if st.button("📌 Hata Kaydet", use_container_width=True, key="btn_hata"):
            if hata_ders and hata_konu:
                kayit = HataKaydi(
                    ders=hata_ders,
                    konu=hata_konu,
                    aciklama=hata_aciklama or "",
                )
                ogr.hata_kaydi_ekle(kayit)
                repo.guncelle(ogr)
                st.success("✅ Hata kaydedildi! Tekrar takvimi oluşturuldu.")
                st.rerun()

    with col_h2:
        st.markdown("#### 📅 Tekrar Takvimi")
        if ogr.hata_kayitlari:
            bugun = date.today()
            yaklasan = []
            for h in ogr.hata_kayitlari:
                sonraki = h.sonraki_tekrar_tarihi()
                if sonraki:
                    gun_fark = (sonraki - bugun).days
                    durum = "🔴 Gecikmiş" if gun_fark < 0 else "🟡 Bugün" if gun_fark == 0 else f"🟢 {gun_fark} gün"
                    yaklasan.append({
                        "Ders": h.ders,
                        "Konu": h.konu,
                        "Tekrar": h.tekrar_sayisi,
                        "Sonraki": sonraki.isoformat(),
                        "Durum": durum,
                    })

            if yaklasan:
                yaklasan.sort(key=lambda x: x["Sonraki"])
                st.dataframe(pd.DataFrame(yaklasan), use_container_width=True, hide_index=True)

                # Tekrar yapma butonu
                st.markdown("---")
                for h in ogr.hata_kayitlari:
                    sonraki = h.sonraki_tekrar_tarihi()
                    if sonraki and sonraki <= bugun:
                        if st.button(f"✅ '{h.konu}' tekrarını yaptım", key=f"tekrar_{h.konu}_{h.ders}"):
                            h.tekrar_yap()
                            repo.guncelle(ogr)
                            st.success(f"Tekrar #{h.tekrar_sayisi} kaydedildi!")
                            st.rerun()
            else:
                st.info("🎉 Yaklaşan tekrar yok. Tüm tekrarlar tamamlandı!")
        else:
            st.info("📌 Henüz hata kaydı yok. Sol taraftan yeni hata girebilirsiniz.")


# ──────────────────────────────────────────────
# SEKME 7: PDR NOTLARI
# ──────────────────────────────────────────────
with sekmeler[6]:
    st.subheader("📓 PDR Görüşme Notları")

    col_n1, col_n2 = st.columns([1, 2])
    with col_n1:
        st.markdown("#### ➕ Yeni Görüşme Notu")
        not_tarih = st.date_input("Tarih", date.today(), key="not_tarih")
        not_tur = st.selectbox("Tür", [
            "Bireysel Görüşme", "Veli Görüşmesi", "Kriz Müdahalesi",
            "Yönlendirme", "Takip Notu", "Diğer"
        ], key="not_tur")
        not_icerik = st.text_area("İçerik", key="not_icerik", height=200,
                                   placeholder="Görüşme notlarını buraya yazın...")
        not_etiketler = st.text_input("Etiketler (virgülle ayırın)",
                                       key="not_etiketler",
                                       placeholder="motivasyon, sınav kaygısı")

        if st.button("💾 Notu Kaydet", use_container_width=True, key="btn_not"):
            if not_icerik.strip():
                etiket_list = [e.strip() for e in not_etiketler.split(",") if e.strip()]
                not_kaydi = GorusmeNotu(
                    tarih=not_tarih,
                    tur=not_tur,
                    icerik=not_icerik.strip(),
                    etiketler=etiket_list,
                )
                ogr.gorusme_notu_ekle(not_kaydi)
                repo.guncelle(ogr)
                st.success("✅ Not kaydedildi!")
                st.rerun()

    with col_n2:
        st.markdown("#### 📋 Geçmiş Notlar")
        if ogr.gorusme_notlari:
            for not_k in reversed(ogr.gorusme_notlari):
                with st.expander(f"📄 {not_k.tarih.isoformat()} – {not_k.tur}"):
                    st.write(not_k.icerik)
                    if not_k.etiketler:
                        etiketler_html = " ".join(
                            f'<span style="background:rgba(108,99,255,0.2);color:#6C63FF;padding:2px 8px;border-radius:10px;font-size:0.8rem;margin:2px;">{e}</span>'
                            for e in not_k.etiketler
                        )
                        st.markdown(etiketler_html, unsafe_allow_html=True)
        else:
            st.info("📝 Henüz görüşme notu yok.")
