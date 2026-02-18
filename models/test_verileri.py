"""
OmniPDR – models/test_verileri.py
===================================
PDR testleri, envanterleri ve ölçekleri için statik veri seti.
İçerik:
1. Sınav Kaygısı Ölçeği
2. Holland Mesleki İlgi Envanteri (Kısa Sürüm)
3. Çalışma Davranışı Değerlendirme Ölçeği
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

@dataclass
class TestSorusu:
    id: int
    metin: str
    secenekler: Optional[List[str]] = None
    puanlar: Optional[List[int]] = None
    kategori: Optional[str] = None  # Holland tipi vb. için

@dataclass
class PDRTesti:
    id: str
    ad: str
    aciklama: str
    sorular: List[TestSorusu]
    degerlendirme_tipi: str  # "toplam_puan", "kategori_puani"

# ──────────────────────────────────────────────
# 1. Sınav Kaygısı Ölçeği
# ──────────────────────────────────────────────
SINAV_KAYGISI_SORULARI = [
    "Sınavdan bir gün öncesinde huzursuz olurum.",
    "Sınav anında bildiklerimi unuturum diye endişelenirim.",
    "Sınav sırasında kalbim hızlı çarpar.",
    "Sınavdayken zamanın yetmeyeceğini düşünürüm.",
    "Başkalarının benden daha başarılı olacağını düşünürüm.",
    "Sınav sonuçlarının geleceğimi tamamen belirleyeceğini düşünürüm.",
    "Sınavda başarısız olursam ailemin güvenini sarsarım.",
    "Sınav anında midemde kasılmalar veya ağrılar olur.",
    "Sınavdan sonra 'keşke daha fazla çalışsaydım' diye kendimi suçlarım.",
    "Sınav kelimesini duymak bile beni gerer."
]

# ──────────────────────────────────────────────
# 2. Holland Mesleki İlgi Envanteri (Kısa)
# ──────────────────────────────────────────────
# R: Gerçekçi, I: Araştırmacı, A: Sanatsal, S: Sosyal, E: Girişimci, C: Geleneksel
HOLLAND_SORULARI = [
    (1, "R", "Bozulan eşyaları tamir etmekten hoşlanırım."),
    (2, "I", "Bilimsel deneyler yapmayı severim."),
    (3, "A", "Resim yapmak veya enstrüman çalmak beni mutlu eder."),
    (4, "S", "İnsanlara yardımcı olmak ve sorunlarını dinlemek isterim."),
    (5, "E", "Bir grubu yönetmek ve ikna etmek benim işim."),
    (6, "C", "Düzenli not tutmak ve planlı çalışmak hoşuma gider."),
    (7, "R", "Doğa yürüyüşleri ve açık hava etkinliklerini severim."),
    (8, "I", "Karmaşık problemleri çözmekten zevk alırım."),
    (9, "A", "Yaratıcı yazılar yazmak veya tasarım yapmak ilgimi çeker."),
    (10, "S", "Arkadaşlarımla sohbet etmek ve etkinlik organize etmek isterim."),
    (11, "E", "Yeni bir ürün pazarlamak veya satış yapmak heyecan vericidir."),
    (12, "C", "Rakamlarla uğraşmak ve hesap yapmak benim için kolaydır.")
]

def tum_testleri_getir() -> List[PDRTesti]:
    return [
        PDRTesti(
            id="sinav_kaygisi",
            ad="Sınav Kaygısı Ölçeği",
            aciklama="Sınava yönelik kaygı düzeyinizi ölçer.",
            sorular=[TestSorusu(i+1, s) for i, s in enumerate(SINAV_KAYGISI_SORULARI)],
            degerlendirme_tipi="toplam_puan"
        ),
        PDRTesti(
            id="holland_ilgi",
            ad="Holland Mesleki İlgi Envanteri",
            aciklama="İlgi alanlarınıza göre uygun meslek tiplerini belirler.",
            # (id, kategori, metin)
            sorular=[TestSorusu(id=i, metin=m, kategori=k) for i, k, m in HOLLAND_SORULARI],
            degerlendirme_tipi="kategori_puani"
        )
    ]
