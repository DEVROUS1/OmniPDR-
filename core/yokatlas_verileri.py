"""
OmniPDR – core/yokatlas_verileri.py
=======================================
YÖK Atlas statik veri seti.

En popüler ~80 üniversite bölümünün 2024 YKS taban puanları,
başarı sıralamaları ve kontenjan bilgileri.

Not: Veriler yaklaşık değerlerdir ve bilgi amaçlıdır.
Resmi güncel veriler için: https://yokatlas.yok.gov.tr
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class BolumBilgisi:
    """Bir üniversite bölümünü temsil eder."""
    universite: str
    bolum: str
    sehir: str
    puan_turu: str          # SAY, EA, SOZ, TYT, YDT
    taban_puan: float       # 2024 taban puanı
    tavan_puan: float       # 2024 tavan puanı
    siralama: int           # 2024 başarı sıralaması
    kontenjan: int          # Toplam kontenjan
    tur: str = "Devlet"     # Devlet / Vakıf


# ──────────────────────────────────────────────
# YKS 2024 Taban Puanları (Yaklaşık Değerler)
# ──────────────────────────────────────────────
BOLUM_VERILERI: List[BolumBilgisi] = [
    # ── TIP ────────────────────────────────────
    BolumBilgisi("Hacettepe Üniversitesi", "Tıp", "Ankara", "SAY", 489.2, 498.5, 748, 350),
    BolumBilgisi("İstanbul Üniversitesi", "Tıp", "İstanbul", "SAY", 486.1, 497.8, 1100, 450),
    BolumBilgisi("Ankara Üniversitesi", "Tıp", "Ankara", "SAY", 482.5, 495.2, 2200, 400),
    BolumBilgisi("Ege Üniversitesi", "Tıp", "İzmir", "SAY", 479.8, 493.6, 3500, 350),
    BolumBilgisi("Gazi Üniversitesi", "Tıp", "Ankara", "SAY", 478.3, 492.1, 4200, 320),
    BolumBilgisi("Dokuz Eylül Üniversitesi", "Tıp", "İzmir", "SAY", 475.2, 490.8, 5800, 300),
    BolumBilgisi("Erciyes Üniversitesi", "Tıp", "Kayseri", "SAY", 460.5, 480.3, 18000, 300),
    BolumBilgisi("İnönü Üniversitesi", "Tıp", "Malatya", "SAY", 455.2, 475.1, 25000, 280),

    # ── DİŞ HEKİMLİĞİ ────────────────────────
    BolumBilgisi("Hacettepe Üniversitesi", "Diş Hekimliği", "Ankara", "SAY", 472.5, 488.3, 7200, 100),
    BolumBilgisi("İstanbul Üniversitesi", "Diş Hekimliği", "İstanbul", "SAY", 468.7, 485.1, 9800, 120),

    # ── ECZACILIK ──────────────────────────────
    BolumBilgisi("Hacettepe Üniversitesi", "Eczacılık", "Ankara", "SAY", 462.1, 478.5, 16000, 150),
    BolumBilgisi("İstanbul Üniversitesi", "Eczacılık", "İstanbul", "SAY", 458.3, 475.2, 20000, 160),

    # ── BİLGİSAYAR MÜHENDİSLİĞİ ──────────────
    BolumBilgisi("ODTÜ", "Bilgisayar Mühendisliği", "Ankara", "SAY", 478.9, 496.1, 3800, 180),
    BolumBilgisi("Boğaziçi Üniversitesi", "Bilgisayar Mühendisliği", "İstanbul", "SAY", 482.3, 497.2, 2400, 120),
    BolumBilgisi("İTÜ", "Bilgisayar Mühendisliği", "İstanbul", "SAY", 475.6, 493.8, 5500, 180),
    BolumBilgisi("Hacettepe Üniversitesi", "Bilgisayar Mühendisliği", "Ankara", "SAY", 470.2, 490.1, 8500, 150),
    BolumBilgisi("Yıldız Teknik Üniversitesi", "Bilgisayar Mühendisliği", "İstanbul", "SAY", 458.1, 480.5, 20500, 150),
    BolumBilgisi("Ankara Üniversitesi", "Bilgisayar Mühendisliği", "Ankara", "SAY", 445.2, 470.3, 38000, 120),

    # ── ELEKTRİK-ELEKTRONİK MÜHENDİSLİĞİ ────
    BolumBilgisi("ODTÜ", "Elektrik-Elektronik Mühendisliği", "Ankara", "SAY", 472.5, 492.3, 7000, 200),
    BolumBilgisi("İTÜ", "Elektrik-Elektronik Mühendisliği", "İstanbul", "SAY", 465.8, 488.1, 12500, 180),
    BolumBilgisi("Boğaziçi Üniversitesi", "Elektrik-Elektronik Mühendisliği", "İstanbul", "SAY", 474.1, 494.5, 6200, 120),

    # ── MAKİNE MÜHENDİSLİĞİ ──────────────────
    BolumBilgisi("ODTÜ", "Makine Mühendisliği", "Ankara", "SAY", 465.2, 488.5, 13000, 240),
    BolumBilgisi("İTÜ", "Makine Mühendisliği", "İstanbul", "SAY", 460.8, 485.2, 17000, 220),

    # ── İNŞAAT MÜHENDİSLİĞİ ──────────────────
    BolumBilgisi("ODTÜ", "İnşaat Mühendisliği", "Ankara", "SAY", 448.5, 478.2, 32000, 220),
    BolumBilgisi("İTÜ", "İnşaat Mühendisliği", "İstanbul", "SAY", 443.2, 472.5, 40000, 200),

    # ── ENDÜSTRİ MÜHENDİSLİĞİ ────────────────
    BolumBilgisi("Boğaziçi Üniversitesi", "Endüstri Mühendisliği", "İstanbul", "SAY", 470.8, 491.2, 8200, 100),
    BolumBilgisi("ODTÜ", "Endüstri Mühendisliği", "Ankara", "SAY", 462.5, 485.8, 15500, 150),

    # ── MİMARLIK ──────────────────────────────
    BolumBilgisi("İTÜ", "Mimarlık", "İstanbul", "SAY", 452.3, 478.1, 28000, 120),
    BolumBilgisi("ODTÜ", "Mimarlık", "Ankara", "SAY", 448.1, 475.3, 33000, 100),

    # ── HUKUK ──────────────────────────────────
    BolumBilgisi("Ankara Üniversitesi", "Hukuk", "Ankara", "EA", 442.5, 468.3, 12000, 450),
    BolumBilgisi("İstanbul Üniversitesi", "Hukuk", "İstanbul", "EA", 445.8, 472.1, 10000, 500),
    BolumBilgisi("Marmara Üniversitesi", "Hukuk", "İstanbul", "EA", 438.2, 462.5, 15000, 400),
    BolumBilgisi("Galatasaray Üniversitesi", "Hukuk", "İstanbul", "EA", 450.1, 475.8, 7500, 100),
    BolumBilgisi("Hacettepe Üniversitesi", "Hukuk", "Ankara", "EA", 440.3, 465.2, 13500, 200),

    # ── PSİKOLOJİ ─────────────────────────────
    BolumBilgisi("ODTÜ", "Psikoloji", "Ankara", "EA", 435.2, 460.8, 18000, 100),
    BolumBilgisi("Boğaziçi Üniversitesi", "Psikoloji", "İstanbul", "EA", 440.8, 465.3, 14000, 80),
    BolumBilgisi("Hacettepe Üniversitesi", "Psikoloji", "Ankara", "EA", 432.1, 458.5, 20000, 100),

    # ── İŞLETME ───────────────────────────────
    BolumBilgisi("Boğaziçi Üniversitesi", "İşletme", "İstanbul", "EA", 445.6, 470.2, 10500, 120),
    BolumBilgisi("ODTÜ", "İşletme", "Ankara", "EA", 430.1, 455.8, 22000, 120),
    BolumBilgisi("İstanbul Üniversitesi", "İşletme", "İstanbul", "EA", 410.5, 440.2, 48000, 300),

    # ── İKTİSAT ───────────────────────────────
    BolumBilgisi("Boğaziçi Üniversitesi", "İktisat", "İstanbul", "EA", 448.2, 472.5, 9000, 100),
    BolumBilgisi("ODTÜ", "İktisat", "Ankara", "EA", 425.5, 452.3, 26000, 100),

    # ── ÖĞRETMENLİK ──────────────────────────
    BolumBilgisi("Hacettepe Üniversitesi", "PDR (Rehberlik)", "Ankara", "EA", 415.2, 445.1, 42000, 80),
    BolumBilgisi("Ankara Üniversitesi", "Sınıf Öğretmenliği", "Ankara", "EA", 388.5, 420.3, 85000, 120),
    BolumBilgisi("Gazi Üniversitesi", "Matematik Öğretmenliği", "Ankara", "SAY", 420.1, 448.5, 60000, 100),
    BolumBilgisi("Hacettepe Üniversitesi", "İngilizce Öğretmenliği", "Ankara", "YDT", 425.3, 455.2, 5000, 80),

    # ── HEMŞİRELİK ───────────────────────────
    BolumBilgisi("Hacettepe Üniversitesi", "Hemşirelik", "Ankara", "SAY", 395.2, 430.5, 120000, 200),
    BolumBilgisi("İstanbul Üniversitesi", "Hemşirelik", "İstanbul", "SAY", 388.5, 422.1, 145000, 250),

    # ── SÖZEL BÖLÜMLER ────────────────────────
    BolumBilgisi("Ankara Üniversitesi", "Tarih", "Ankara", "SOZ", 380.5, 415.2, 28000, 150),
    BolumBilgisi("İstanbul Üniversitesi", "Türk Dili ve Edebiyatı", "İstanbul", "SOZ", 375.2, 410.5, 35000, 200),
    BolumBilgisi("Ankara Üniversitesi", "Felsefe", "Ankara", "SOZ", 365.8, 400.2, 48000, 100),
    BolumBilgisi("Marmara Üniversitesi", "İlahiyat", "İstanbul", "SOZ", 360.1, 395.5, 55000, 300),

    # ── TYT İLE YERLEŞEN BÖLÜMLER ─────────────
    BolumBilgisi("Anadolu Üniversitesi", "Adalet (Ön Lisans)", "Eskişehir", "TYT", 280.5, 340.2, 350000, 500),
    BolumBilgisi("İstanbul Üniversitesi", "Sağlık Yönetimi (Ön Lisans)", "İstanbul", "TYT", 295.3, 355.1, 280000, 200),
    BolumBilgisi("Ankara Üniversitesi", "Çocuk Gelişimi (Ön Lisans)", "Ankara", "TYT", 270.8, 330.5, 400000, 150),

    # ── VAKIF ÜNİVERSİTELERİ ──────────────────
    BolumBilgisi("Koç Üniversitesi", "Tıp", "İstanbul", "SAY", 485.5, 497.8, 1300, 100, "Vakıf"),
    BolumBilgisi("Koç Üniversitesi", "Bilgisayar Mühendisliği", "İstanbul", "SAY", 468.2, 490.5, 10000, 80, "Vakıf"),
    BolumBilgisi("Sabancı Üniversitesi", "Mühendislik", "İstanbul", "SAY", 455.8, 482.3, 23000, 150, "Vakıf"),
    BolumBilgisi("Bilkent Üniversitesi", "Bilgisayar Mühendisliği", "Ankara", "SAY", 462.5, 485.8, 15000, 100, "Vakıf"),
    BolumBilgisi("Koç Üniversitesi", "Hukuk", "İstanbul", "EA", 455.2, 478.3, 5800, 80, "Vakıf"),
    BolumBilgisi("Özyeğin Üniversitesi", "İşletme", "İstanbul", "EA", 390.5, 425.8, 75000, 120, "Vakıf"),
]


# ──────────────────────────────────────────────
# Arama ve Filtreleme Fonksiyonları
# ──────────────────────────────────────────────
def bolum_ara(
    puan_turu: Optional[str] = None,
    min_puan: Optional[float] = None,
    max_puan: Optional[float] = None,
    sehir: Optional[str] = None,
    bolum_adi: Optional[str] = None,
    tur: Optional[str] = None,
) -> List[BolumBilgisi]:
    """Kriterlere göre bölüm arar."""
    sonuclar = BOLUM_VERILERI.copy()

    if puan_turu:
        sonuclar = [b for b in sonuclar if b.puan_turu == puan_turu]
    if min_puan is not None:
        sonuclar = [b for b in sonuclar if b.taban_puan >= min_puan]
    if max_puan is not None:
        sonuclar = [b for b in sonuclar if b.taban_puan <= max_puan]
    if sehir:
        sonuclar = [b for b in sonuclar if sehir.lower() in b.sehir.lower()]
    if bolum_adi:
        sonuclar = [b for b in sonuclar if bolum_adi.lower() in b.bolum.lower()]
    if tur:
        sonuclar = [b for b in sonuclar if b.tur == tur]

    return sorted(sonuclar, key=lambda b: b.taban_puan, reverse=True)


def universite_oner(
    puan: float,
    puan_turu: str,
    tolerans: float = 20.0,
) -> Dict[str, List[BolumBilgisi]]:
    """
    Puana göre üniversite önerileri.
    3 kategori: Güvenli, Dengeli, Şans
    """
    tum = bolum_ara(puan_turu=puan_turu)

    guvenli = [b for b in tum if b.taban_puan <= puan - tolerans / 2][:8]
    dengeli = [b for b in tum if abs(b.taban_puan - puan) <= tolerans / 2][:8]
    sans = [b for b in tum if puan < b.taban_puan <= puan + tolerans][:8]

    return {
        "guvenli": sorted(guvenli, key=lambda b: b.taban_puan, reverse=True),
        "dengeli": sorted(dengeli, key=lambda b: b.taban_puan, reverse=True),
        "sans": sorted(sans, key=lambda b: b.taban_puan),
    }


def benzersiz_sehirler() -> List[str]:
    """Verideki tüm şehirleri döndürür."""
    return sorted(set(b.sehir for b in BOLUM_VERILERI))


def benzersiz_bolumler() -> List[str]:
    """Verideki tüm bölüm adlarını döndürür."""
    return sorted(set(b.bolum for b in BOLUM_VERILERI))


def benzersiz_universiteler() -> List[str]:
    """Verideki tüm üniversite adlarını döndürür."""
    return sorted(set(b.universite for b in BOLUM_VERILERI))
