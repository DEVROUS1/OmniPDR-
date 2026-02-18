"""
OmniPDR – arayuz_app.py
===========================
Streamlit tabanlı ana dashboard. Tüm modülleri bir araya getirir.

Çalıştırma:
    streamlit run arayuz_app.py

Mimari:
    ┌─────────────────────────────────┐
    │  Streamlit (Sunum Katmanı)     │
    │  arayuz_app.py                  │
    ├─────────────────────────────────┤
    │  Servis Katmanı                │
    │  core/analiz_motoru.py          │
    │  core/veritabani.py             │
    ├─────────────────────────────────┤
    │  Domain Katmanı                │
    │  models/ogrenci_sinifi.py       │
    └─────────────────────────────────┘
"""

from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Proje kök dizinini path'e ekle ──────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from core.analiz_motoru import AnalizMotoru, UyariSeviyesi
from core.veritabani import OgrenciRepository
from models.ogrenci_sinifi import DenemeKaydi, Ogrenci

# ──────────────────────────────────────────────
# Sayfa Konfigürasyonu
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="OmniPDR – Bütünsel Analiz Sistemi",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Global CSS (koyu tema, özel renkler)
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Ana arka plan */
.stApp {
    background: linear-gradient(135deg, #0D1117 0%, #161B22 50%, #0D1117 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161B22 0%, #0D1117 100%);
    border-right: 1px solid #30363D;
}

/* Metrik kartları */
[data-testid="stMetric"] {
    background: #1C2128;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 16px;
}

/* Başlıklar */
h1, h2, h3 { color: #E6EDF3 !important; }
p, label, .stMarkdown { color: #8B949E; }

/* Uyarı renkleri */
.kritik { background: #3D1F1F; border: 1px solid #F85149; border-radius: 10px; padding: 14px; }
.uyari  { background: #2D2208; border: 1px solid #F0883E; border-radius: 10px; padding: 14px; }
.dikkat { background: #1C2D1C; border: 1px solid #3FB950; border-radius: 10px; padding: 14px; }
.normal { background: #1C2128; border: 1px solid #388BFD; border-radius: 10px; padding: 14px; }

/* ZPD göstergesi */
.zpd-box {
    background: linear-gradient(90deg, #1C2128, #21262D);
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 18px;
    margin: 8px 0;
}

/* Başlık banner */
.banner {
    background: linear-gradient(90deg, #1A2332 0%, #1F3040 50%, #1A2332 100%);
    border: 1px solid #388BFD30;
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
}

.mono { font-family: 'JetBrains Mono', monospace; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Durum Yönetimi
# ──────────────────────────────────────────────
@st.cache_resource
def repo_yukle() -> OgrenciRepository:
    """Repository'yi bir kez yükle, uygulama boyunca paylaş."""
    return OgrenciRepository()


def secili_ogrenci() -> Ogrenci | None:
    """Session state'ten seçili öğrenciyi döndürür."""
    return st.session_state.get("aktif_ogrenci")


# ──────────────────────────────────────────────
# Grafik Yardımcıları
# ──────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_dark"
RENK_PALETI = ["#388BFD", "#3FB950", "#F0883E", "#F85149",
               "#BC8CFF", "#58A6FF", "#79C0FF", "#56D364"]


def net_trend_grafigi(ogrenci: Ogrenci) -> go.Figure:
    """Zaman vs. Toplam Net (çizgi + scatter + area)."""
    kayitlar = ogrenci.deneme_kayitlari
    if not kayitlar:
        return go.Figure().update_layout(title="Henüz deneme verisi yok")

    df = pd.DataFrame([
        {"Tarih": k.tarih, "Toplam Net": k.toplam_net,
         "Stres": k.stres_puani, "Çalışma (saat)": k.calisma_saati}
        for k in kayitlar
    ])

    fig = go.Figure()

    # Alan dolgu
    fig.add_trace(go.Scatter(
        x=df["Tarih"], y=df["Toplam Net"],
        fill="tozeroy", fillcolor="rgba(56, 139, 253, 0.08)",
        line=dict(color="#388BFD", width=2.5),
        mode="lines+markers",
        marker=dict(size=9, color="#388BFD", line=dict(color="#161B22", width=2)),
        name="Toplam Net",
        hovertemplate="<b>%{x|%d %b}</b><br>Net: %{y:.1f}<extra></extra>",
    ))

    # Hedef çizgisi
    if ogrenci.hedef_net:
        fig.add_hline(
            y=ogrenci.hedef_net,
            line_dash="dot",
            line_color="#3FB950",
            annotation_text=f"🎯 Hedef: {ogrenci.hedef_net:.0f}",
            annotation_position="top right",
        )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",
        title=dict(text="📈 Net Trendi", font=dict(size=16, color="#E6EDF3")),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(gridcolor="#21262D", title="Toplam Net"),
        margin=dict(l=10, r=10, t=50, b=10),
        height=320,
    )
    return fig


def ders_bazli_net_grafigi(ogrenci: Ogrenci) -> go.Figure:
    """Her ders için son deneme netlerini gösteren bar grafiği."""
    son = ogrenci.son_deneme
    if not son:
        return go.Figure()

    dersler = list(son.netleri.keys())
    netler = list(son.netleri.values())

    fig = px.bar(
        x=dersler, y=netler,
        color=netler,
        color_continuous_scale=["#F85149", "#F0883E", "#388BFD", "#3FB950"],
        text=[f"{n:.1f}" for n in netler],
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(
        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",
        title=dict(text="📊 Ders Bazlı Netler (Son Deneme)", font=dict(size=16, color="#E6EDF3")),
        xaxis_title="",
        yaxis_title="Net",
        coloraxis_showscale=False,
        height=320,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def stres_calisma_grafigi(ogrenci: Ogrenci) -> go.Figure:
    """Çalışma saati vs. Stres puanı vs. Net — kabarcık grafiği."""
    kayitlar = ogrenci.deneme_kayitlari
    if len(kayitlar) < 2:
        return go.Figure().update_layout(title="Yeterli veri yok (min. 2 kayıt)")

    df = pd.DataFrame([
        {
            "Çalışma (saat)": k.calisma_saati,
            "Stres Puanı": k.stres_puani,
            "Toplam Net": k.toplam_net,
            "Tarih": k.tarih.strftime("%d %b"),
        }
        for k in kayitlar
    ])

    fig = px.scatter(
        df,
        x="Çalışma (saat)", y="Stres Puanı",
        size="Toplam Net", color="Toplam Net",
        hover_data=["Tarih", "Toplam Net"],
        color_continuous_scale="RdYlGn",
        size_max=40,
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(
        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",
        title=dict(
            text="🔮 Çalışma Saati × Stres × Net Korelasyonu",
            font=dict(size=16, color="#E6EDF3"),
        ),
        xaxis=dict(gridcolor="#21262D", title="Haftalık Çalışma Saati"),
        yaxis=dict(gridcolor="#21262D", title="Stres Puanı (1–10)"),
        height=340,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def radar_grafigi(ogrenci: Ogrenci) -> go.Figure:
    """Son 2 denemeyi karşılaştıran radar/spider grafiği."""
    kayitlar = ogrenci.deneme_kayitlari
    if len(kayitlar) < 1:
        return go.Figure()

    # Ortak dersler
    if len(kayitlar) >= 2:
        onceki = kayitlar[-2]
        son = kayitlar[-1]
        dersler = [d for d in son.netleri if d in onceki.netleri]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[onceki.netleri[d] for d in dersler],
            theta=dersler, fill="toself",
            fillcolor="rgba(56,139,253,0.15)",
            line_color="#388BFD",
            name=f"Önceki ({onceki.tarih})",
        ))
        fig.add_trace(go.Scatterpolar(
            r=[son.netleri[d] for d in dersler],
            theta=dersler, fill="toself",
            fillcolor="rgba(63,185,80,0.15)",
            line_color="#3FB950",
            name=f"Son ({son.tarih})",
        ))
    else:
        son = kayitlar[-1]
        dersler = list(son.netleri.keys())
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=list(son.netleri.values()),
            theta=dersler, fill="toself",
            fillcolor="rgba(56,139,253,0.15)",
            line_color="#388BFD",
            name=f"Son Deneme ({son.tarih})",
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="#161B22",
            radialaxis=dict(gridcolor="#30363D", linecolor="#30363D"),
            angularaxis=dict(linecolor="#30363D"),
        ),
        paper_bgcolor="#161B22",
        legend=dict(font=dict(color="#8B949E")),
        title=dict(text="🕸️ Ders Radar Analizi", font=dict(size=16, color="#E6EDF3")),
        height=360,
        margin=dict(l=60, r=60, t=60, b=60),
    )
    return fig


def tekrar_takvim_grafigi(ogrenci: Ogrenci) -> go.Figure:
    """Önümüzdeki 30 günlük Ebbinghaus tekrar takvimini görselleştirir."""
    bugun = date.today()
    takvim: dict[date, list[str]] = {}

    for h in ogrenci.hata_kayitlari:
        for t in h.tekrar_tarihleri:
            if t >= bugun and t not in h.tamamlanan_tekrarlar:
                takvim.setdefault(t, []).append(f"{h.ders}: {h.konu}")

    if not takvim:
        return go.Figure().update_layout(
            title="📅 Tekrar Takvimi – Bekleyen tekrar yok",
            paper_bgcolor="#161B22",
        )

    satirlar = []
    for gun, konular in sorted(takvim.items()):
        for k in konular:
            satirlar.append({"Tarih": gun, "Konu": k, "Sayı": 1})

    df = pd.DataFrame(satirlar)
    fig = px.bar(
        df.groupby("Tarih").size().reset_index(name="Tekrar Sayısı"),
        x="Tarih", y="Tekrar Sayısı",
        template=PLOTLY_TEMPLATE,
        color="Tekrar Sayısı",
        color_continuous_scale=["#388BFD", "#F85149"],
    )
    fig.update_layout(
        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",
        title=dict(text="📅 Ebbinghaus Tekrar Takvimi (30 Gün)", font=dict(size=16, color="#E6EDF3")),
        xaxis_title="",
        yaxis_title="Tekrar Sayısı",
        coloraxis_showscale=False,
        height=280,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
def render_sidebar(repo: OgrenciRepository) -> None:
    """Sol panel: öğrenci seçimi ve hızlı veri girişi."""
    with st.sidebar:
        st.markdown("## 🧠 OmniPDR")
        st.markdown("*Bütünsel Bilişsel & Duygusal Analiz*")
        st.divider()

        # ── Öğrenci seçimi ──────────────────────
        ogrenciler = repo.hepsini_getir()
        secenekler = {o.ad: o for o in ogrenciler}

        st.subheader("👤 Öğrenci Seç")
        secim = st.selectbox(
            "Kayıtlı Öğrenciler",
            options=["— Seçiniz —"] + list(secenekler.keys()),
            key="ogrenci_secim",
        )
        if secim != "— Seçiniz —":
            st.session_state["aktif_ogrenci"] = secenekler[secim]
        elif "aktif_ogrenci" not in st.session_state:
            st.session_state["aktif_ogrenci"] = None

        st.divider()

        # ── Yeni Öğrenci ──────────────────────
        with st.expander("➕ Yeni Öğrenci Ekle", expanded=False):
            yeni_ad = st.text_input("Ad Soyad", placeholder="Ahmet Yılmaz")
            yeni_hedef = st.text_input("Hedef Bölüm", placeholder="Tıp – Hacettepe")
            yeni_sinav = st.radio("Sınav Türü", ["YKS", "LGS"], horizontal=True)
            yeni_net = st.number_input(
                "Hedef Toplam Net", min_value=0.0, max_value=500.0, step=5.0, value=0.0
            )
            if st.button("🚀 Öğrenci Oluştur", use_container_width=True):
                if yeni_ad.strip():
                    ogr = Ogrenci(
                        ad=yeni_ad.strip(),
                        hedef_bolum=yeni_hedef.strip(),
                        sinav_turu=yeni_sinav,
                        hedef_net=yeni_net if yeni_net > 0 else None,
                    )
                    repo.kaydet(ogr)
                    st.session_state["aktif_ogrenci"] = ogr
                    st.success(f"✅ {yeni_ad} oluşturuldu!")
                    st.rerun()
                else:
                    st.error("Ad alanı boş bırakılamaz.")

        st.divider()

        # ── Hızlı Deneme Girişi ──────────────
        ogr = secili_ogrenci()
        if ogr:
            with st.expander("📝 Yeni Deneme Kaydı", expanded=True):
                tarih = st.date_input("Tarih", value=date.today())
                st.markdown("**Ders Netleri**")
                netleri = {}
                cols = st.columns(2)
                for i, ders in enumerate(ogr.dersler):
                    with cols[i % 2]:
                        netleri[ders] = st.number_input(
                            ders, min_value=0.0, max_value=40.0,
                            step=0.5, value=0.0, key=f"net_{ders}"
                        )

                st.markdown("**Bütünsel Veriler (Zimmerman)**")
                calisma = st.slider("Haftalık Çalışma Saati", 0.0, 80.0, 40.0, 0.5)
                stres = st.slider("Stres Puanı (1–10)", 1, 10, 5)
                uyku = st.slider("Günlük Ortalama Uyku (saat)", 3.0, 10.0, 7.0, 0.5)
                notlar = st.text_area("Not (opsiyonel)", placeholder="Bu haftaki gözlemler...", height=60)

                if st.button("💾 Kaydı Ekle", use_container_width=True):
                    kayit = DenemeKaydi(
                        tarih=tarih,
                        netleri={k: v for k, v in netleri.items()},
                        calisma_saati=calisma,
                        stres_puani=stres,
                        uyku_saati=uyku,
                        notlar=notlar,
                    )
                    ogr.deneme_ekle(kayit)
                    repo.kaydet(ogr)
                    AnalizMotoru(ogr).df_sifirla()
                    st.success("✅ Deneme kaydedildi!")
                    st.rerun()

        st.divider()
        st.caption(f"🗄️ Toplam Öğrenci: **{repo.toplam_ogrenci}**")
        st.caption("OmniPDR v2.0 | Ebbinghaus · Vygotsky · Zimmerman")


# ──────────────────────────────────────────────
# Ana Ekran Bölümleri
# ──────────────────────────────────────────────
def render_profil_banner(ogr: Ogrenci, rapor) -> None:
    """Öğrenci profil kartı ve özet metrikler."""
    st.markdown(f"""
    <div class="banner">
        <h2 style="margin:0; color:#E6EDF3;">🎓 {ogr.ad}</h2>
        <p style="margin:4px 0 0 0; color:#8B949E;">
            {ogr.sinav_turu} · {ogr.hedef_bolum} 
            {'· 🎯 Hedef: ' + str(int(ogr.hedef_net)) + ' net' if ogr.hedef_net else ''}
        </p>
    </div>
    """, unsafe_allow_html=True)

    son = ogr.son_deneme
    cols = st.columns(5)
    with cols[0]:
        st.metric("📋 Deneme Sayısı", len(ogr.deneme_kayitlari))
    with cols[1]:
        st.metric("🔢 Son Toplam Net", f"{son.toplam_net:.1f}" if son else "—")
    with cols[2]:
        st.metric("📈 Trend", rapor.haftalik_trend)
    with cols[3]:
        st.metric("🔁 Bekleyen Tekrar", ogr.bekleyen_tekrar_sayisi)
    with cols[4]:
        stres = son.stres_puani if son else "—"
        st.metric("😰 Stres Puanı", stres)


def render_burnout_karti(burnout) -> None:
    """Tükenmişlik uyarı kartı."""
    renk_map = {
        UyariSeviyesi.KRITIK: "kritik",
        UyariSeviyesi.UYARI: "uyari",
        UyariSeviyesi.DIKKAT: "dikkat",
        UyariSeviyesi.NORMAL: "normal",
    }
    css_sinif = renk_map.get(burnout.seviye, "normal")
    st.markdown(f"""
    <div class="{css_sinif}">
        <strong style="font-size:1.05rem;">{burnout.mesaj}</strong>
        <p style="margin:8px 0 0 0; color:#8B949E; font-size:0.9rem;">{burnout.detay}</p>
    </div>
    """, unsafe_allow_html=True)

    if burnout.oneriler:
        with st.expander("💡 Önerilen Eylem Planı", expanded=True):
            for oneri in burnout.oneriler:
                st.markdown(f"• {oneri}")


def render_zpd_karti(zpd) -> None:
    """ZPD göstergesi."""
    st.markdown(f"""
    <div class="zpd-box">
        <h4 style="margin:0; color:#E6EDF3;">🧩 Vygotsky ZPD Analizi</h4>
        <p style="margin:8px 0 2px; color:#8B949E; font-size:0.85rem;">
            Alt Sınır: <span class="mono" style="color:#388BFD;">{zpd.alt_sinir}</span> |
            Mevcut: <span class="mono" style="color:#3FB950;">{zpd.mevcut_seviye:.1f}</span> |
            Üst Sınır: <span class="mono" style="color:#388BFD;">{zpd.ust_sinir}</span> |
            ⭐ Öneri: <span class="mono" style="color:#F0883E;">{zpd.hedef_net}</span>
        </p>
        <p style="margin:4px 0 0 0; color:#E6EDF3; font-size:0.95rem;"><strong>{zpd.durum}</strong></p>
        <p style="margin:2px 0 0 0; color:#8B949E; font-size:0.88rem;">{zpd.aciklama}</p>
    </div>
    """, unsafe_allow_html=True)


def render_hata_paneli(ogr: Ogrenci, repo: OgrenciRepository, motor: AnalizMotoru) -> None:
    """Ebbinghaus hata kaydı ve tekrar takibi."""
    st.subheader("🔁 Ebbinghaus Aralıklı Tekrar")

    # Bugünün tekrarları
    bugun_listesi = ogr.bugunun_tekrar_listesi
    if bugun_listesi:
        st.warning(f"⚠️ Bugün **{len(bugun_listesi)}** konu tekrarlanmalı:")
        for h in bugun_listesi:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"📌 **{h.ders}** – {h.konu}")
            with col2:
                st.caption(f"İlk hata: {h.hata_tarihi}")
            with col3:
                if st.button("✅ Tamamlandı", key=f"tekrar_{h.id}"):
                    h.tekrar_tamamla()
                    repo.kaydet(ogr)
                    st.rerun()
    else:
        st.success("🎉 Bugün bekleyen tekrar yok!")

    # Yeni hata ekle
    with st.expander("➕ Yeni Hata Kaydı Ekle (Ebbinghaus Takvimi)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            h_ders = st.selectbox("Ders", ogr.dersler, key="hata_ders")
        with col2:
            h_konu = st.text_input("Konu / Kazanım", placeholder="Türev uygulamaları – optimizasyon")
        if st.button("📌 Hata Kaydet", use_container_width=True):
            if h_konu.strip():
                h = ogr.hata_ekle(h_ders, h_konu.strip())
                repo.kaydet(ogr)
                st.success(
                    f"✅ Kaydedildi! Tekrar tarihleri: "
                    + ", ".join(t.strftime("%d %b") for t in h.tekrar_tarihleri)
                )
            else:
                st.error("Konu alanı boş bırakılamaz.")

    # Hata yoğunluk tablosu
    df_hata = motor.hata_yogunluk_haritasi()
    if not df_hata.empty:
        st.dataframe(
            df_hata.style.background_gradient(subset=["Hata Sayısı"], cmap="Reds"),
            use_container_width=True,
            hide_index=True,
        )


def render_korelasyon_ozeti(motor: AnalizMotoru) -> None:
    """Çalışma saati/stres/uyku – net Pearson korelasyonları."""
    corr = motor.korelasyon_verisi()
    if not corr:
        return

    st.subheader("🔗 Korelasyon Analizi")
    isim_map = {
        "calisma_saati": ("⏱️ Çalışma Saati", "calisma_saati"),
        "stres_puani":   ("😰 Stres Puanı",   "stres_puani"),
        "uyku_saati":    ("😴 Uyku Süresi",    "uyku_saati"),
    }
    cols = st.columns(3)
    for i, (anahtar, (etiket, _)) in enumerate(isim_map.items()):
        val = corr.get(anahtar, 0.0)
        yorum = ("🟢 Güçlü pozitif" if val > 0.6 else
                 "🟡 Orta pozitif" if val > 0.3 else
                 "🔴 Negatif" if val < -0.3 else "⚪ Zayıf")
        with cols[i]:
            st.metric(etiket, f"r = {val:+.3f}", yorum)


def render_pdr_notlari(ogr: Ogrenci, repo: OgrenciRepository) -> None:
    """PDR görüşme notları yönetimi."""
    st.subheader("📓 PDR Görüşme Notları")

    with st.expander("➕ Yeni Görüşme Notu Ekle", expanded=False):
        icerik = st.text_area("Görüşme İçeriği", height=100,
                              placeholder="Öğrenci sınav kaygısı yaşadığını ifade etti...")
        degerlendirme = st.text_input("Danışman Değerlendirmesi (opsiyonel)",
                                     placeholder="BDT tabanlı yeniden yapılandırma tekniği önerildi.")
        if st.button("💾 Notu Kaydet", use_container_width=True):
            if icerik.strip():
                ogr.gorusme_ekle(icerik.strip(), degerlendirme.strip() or None)
                repo.kaydet(ogr)
                st.success("✅ Görüşme notu kaydedildi!")
            else:
                st.error("Görüşme içeriği boş olamaz.")

    if ogr.gorusme_notlari:
        for not_ in reversed(ogr.gorusme_notlari):
            with st.expander(f"📅 {not_.tarih.strftime('%d %B %Y')} – Görüşme", expanded=False):
                st.markdown(f"**İçerik:** {not_.icerik}")
                if not_.degerlendirme:
                    st.info(f"💬 Danışman: {not_.degerlendirme}")
    else:
        st.info("Henüz görüşme notu eklenmemiş.")


# ──────────────────────────────────────────────
# Ana Render Fonksiyonu
# ──────────────────────────────────────────────
def render_ana_ekran() -> None:
    """Seçili öğrencinin tüm dashboard'unu çizer."""
    ogr = secili_ogrenci()
    if not ogr:
        # Karşılama ekranı
        st.markdown("""
        <div class="banner" style="text-align:center; padding: 48px;">
            <h1 style="font-size:2.5rem; margin:0;">🧠 OmniPDR</h1>
            <p style="font-size:1.1rem; margin:12px 0 0 0; color:#8B949E;">
                Bütünsel Bilişsel ve Duygusal Analiz Sistemi
            </p>
            <p style="margin:16px 0 0 0; color:#58A6FF;">
                Ebbinghaus · Vygotsky · Zimmerman
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.info("👈 Sol panelden bir öğrenci seçin veya yeni öğrenci oluşturun.")
        return

    repo = repo_yukle()
    motor = AnalizMotoru(ogr)
    rapor = motor.tam_analiz()

    # ── Profil Banner ───────────────────────────
    render_profil_banner(ogr, rapor)

    # ── Uyarı Kartları (Full Width) ─────────────
    if rapor.uyku_uyarisi:
        st.warning(rapor.uyku_uyarisi)

    col_burnout, col_zpd = st.columns([1, 1])
    with col_burnout:
        st.subheader("🔥 Tükenmişlik Dedektörü")
        render_burnout_karti(rapor.burnout)
    with col_zpd:
        st.subheader("🧩 ZPD Hedef Analizi")
        render_zpd_karti(rapor.zpd)

    # ── Güçlü / Zayıf Dersler ──────────────────
    if rapor.guclu_dersler or rapor.zayif_dersler:
        c1, c2 = st.columns(2)
        with c1:
            st.success(f"💪 Güçlü Dersler: {', '.join(rapor.guclu_dersler) or '—'}")
        with c2:
            st.error(f"📉 Odaklanılacak Dersler: {', '.join(rapor.zayif_dersler) or '—'}")

    st.divider()

    # ── Grafikler (2 sütun) ─────────────────────
    st.subheader("📊 Performans Grafikleri")
    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(net_trend_grafigi(ogr), use_container_width=True)
    with g2:
        st.plotly_chart(ders_bazli_net_grafigi(ogr), use_container_width=True)

    g3, g4 = st.columns(2)
    with g3:
        st.plotly_chart(stres_calisma_grafigi(ogr), use_container_width=True)
    with g4:
        st.plotly_chart(radar_grafigi(ogr), use_container_width=True)

    # ── Tekrar Takvimi ──────────────────────────
    st.plotly_chart(tekrar_takvim_grafigi(ogr), use_container_width=True)

    # ── Korelasyon Özeti ────────────────────────
    render_korelasyon_ozeti(motor)

    st.divider()

    # ── Alt Paneller ────────────────────────────
    tab1, tab2, tab3 = st.tabs(["🔁 Hata & Tekrar Takibi", "📓 PDR Notları", "📄 Ham Veri"])

    with tab1:
        render_hata_paneli(ogr, repo, motor)
    with tab2:
        render_pdr_notlari(ogr, repo)
    with tab3:
        df = motor.veri_cercevesi()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Henüz deneme verisi girilmemiş.")


# ──────────────────────────────────────────────
# Giriş Noktası
# ──────────────────────────────────────────────
def main() -> None:
    repo = repo_yukle()
    render_sidebar(repo)
    render_ana_ekran()


if __name__ == "__main__":
    main()
