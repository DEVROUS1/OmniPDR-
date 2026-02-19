"""
OmniPDR – models/soru_dagilimi.py
===================================
TYT ve AYT derslerine ait son 5 yılın (2021-2025) konu bazlı soru dağılımı verileri.
2025 verileri, MEB müfredatı ve ÖSYM kazanımlarına dayalı projeksiyonlardır.
"""

from typing import Dict, List

# Yıllar sütunu: 2025, 2024, 2023, 2022, 2021
YILLAR = ["2025", "2024", "2023", "2022", "2021"]

TYT_DAGILIM: Dict[str, Dict[str, List[int]]] = {
    "Türkçe": {
        "Paragraf": [26, 26, 26, 26, 25],
        "Cümlede Anlam": [3, 4, 4, 3, 3],
        "Sözcükte Anlam": [4, 3, 3, 4, 5],
        "Dil Bilgisi (Karma)": [2, 2, 2, 3, 2],
        "Yazım Kuralları": [2, 2, 2, 2, 2],
        "Noktalama İşaretleri": [2, 2, 2, 2, 2],
        "Ses Bilgisi": [1, 1, 1, 0, 1],
    },
    "Temel Matematik": {
        "Problemler": [13, 13, 13, 13, 13],
        "Temel Kavramlar": [3, 3, 1, 2, 3],
        "Sayı Basamakları": [2, 2, 2, 0, 0],
        "Mutlak Değer": [1, 1, 1, 0, 0],
        "Üslü Sayılar": [1, 1, 1, 0, 1],
        "Fonksiyonlar": [1, 1, 1, 1, 1],
        "Kümeler": [1, 1, 1, 1, 1],
        "Olasılık & PKOB": [2, 2, 2, 2, 2],
        "Geometri": [10, 10, 10, 10, 10],
    },
    "Fizik": {
        "Optik": [1, 1, 1, 1, 1],
        "Isı ve Sıcaklık": [1, 1, 1, 1, 1],
        "Elektrik ve Manyetizma": [1, 1, 1, 1, 1],
        "Hareket ve Kuvvet": [1, 1, 1, 1, 1],
        "Madde ve Özellikleri": [1, 1, 1, 1, 1],
        "Basınç ve Kaldırma": [1, 1, 1, 1, 1],
        "Dalgalar": [1, 1, 1, 1, 1],
    },
    "Kimya": {
        "Kimya Bilimi": [1, 1, 1, 1, 1],
        "Atom ve Periyodik Sistem": [1, 1, 1, 1, 1],
        "Maddenin Halleri": [1, 1, 1, 1, 1],
        "Kimyasal Türler Arası Etk.": [1, 1, 1, 1, 1],
        "Karışımlar": [1, 1, 1, 1, 1],
        "Asitler, Bazlar ve Tuzlar": [1, 1, 1, 1, 1],
        "Kimya Her Yerde": [1, 1, 1, 1, 1],
    },
    "Biyoloji": {
        "Canlıların Ortak Özellikleri": [1, 1, 1, 1, 1],
        "Hücre": [1, 1, 1, 1, 1],
        "Canlıların Sınıflandırılması": [1, 1, 1, 1, 1],
        "Hücre Bölünmeleri": [1, 1, 1, 1, 1],
        "Kalıtım": [1, 1, 1, 1, 1],
        "Ekosistem Ekolojisi": [1, 1, 1, 1, 1],
    },
    "Tarih": {
         "Tarih ve Zaman": [1, 1, 1, 1, 1],
         "İlk ve Orta Çağlarda Türk Dünyası": [1, 1, 1, 1, 1],
         "İslam Medeniyeti": [1, 1, 1, 1, 1],
         "Osmanlı Devleti": [1, 1, 1, 1, 1],
         "Milli Mücadele": [1, 1, 1, 1, 1],
    },
    "Coğrafya": {
        "Doğa ve İnsan": [1, 1, 1, 1, 1],
        "Dünyanın Şekli ve Hareketleri": [0, 0, 0, 1, 1],
        "Coğrafi Konum": [1, 1, 1, 0, 0],
        "Harita Bilgisi": [1, 1, 1, 1, 1],
        "Atmosfer ve İklim": [1, 1, 1, 1, 1],
        "Nüfus ve Yerleşme": [1, 1, 1, 1, 1],
    }
}

AYT_DAGILIM: Dict[str, Dict[str, List[int]]] = {
    "Matematik": {
        "Trigonometri": [5, 5, 4, 4, 4],
        "Türev": [4, 4, 3, 3, 3],
        "İntegral": [4, 4, 3, 3, 3],
        "Limit": [2, 2, 2, 2, 2],
        "Logaritma": [2, 2, 2, 2, 2],
        "Diziler": [1, 1, 1, 1, 1],
        "Fonksiyonlar": [2, 2, 2, 2, 2],
        "Polinomlar": [2, 2, 1, 1, 1],
        "Parabol": [0, 1, 1, 1, 1],
        "Geometri": [10, 10, 10, 10, 10],
    },
    "Fizik": {
        "Çembersel Hareket": [2, 2, 2, 2, 2],
        "Basit Harmonik Hareket": [1, 1, 1, 1, 1],
        "İtme ve Momentum": [1, 1, 1, 1, 1],
        "Elektrik Alan ve Potansiyel": [2, 2, 2, 2, 2],
        "Manyetizma ve İndüksiyon": [2, 2, 2, 2, 2],
        "Modern Fizik": [2, 2, 2, 2, 2],
        "Atom Fiziği": [1, 1, 1, 1, 1],
        "Fotoelektrik & Compton": [1, 1, 1, 1, 1],
        "Radyoaktivite": [1, 1, 0, 0, 0],
    },
    "Kimya": {
        "Modern Atom Teorisi": [1, 1, 1, 1, 1],
        "Gazlar": [1, 1, 1, 1, 1],
        "Sıvı Çözeltiler": [1, 2, 1, 1, 1],
        "Kimyasal Enerji": [1, 1, 1, 1, 1],
        "Kimyasal Hız": [1, 1, 1, 1, 1],
        "Kimyasal Denge": [1, 1, 1, 1, 1],
        "Asit-Baz Dengesi": [1, 1, 1, 1, 1],
        "Elektrokimya": [2, 2, 2, 2, 2],
        "Organik Kimya": [3, 3, 3, 3, 3],
    },
    "Biyoloji": {
        "Sinir Sistemi": [1, 1, 1, 1, 1],
        "Endokrin Sistem": [1, 1, 1, 1, 1],
        "Duyu Organları": [1, 1, 1, 1, 1],
        "Destek ve Hareket": [1, 1, 0, 0, 1],
        "Dolaşım Sistemi": [1, 1, 1, 1, 1],
        "Solunum Sistemi": [1, 1, 1, 1, 1],
        "Protein Sentezi": [2, 2, 2, 2, 1],
        "Fotosentez/Kemosentez": [1, 1, 1, 1, 1],
        "Hücre Solunumu": [1, 1, 1, 1, 1],
        "Bitki Biyolojisi": [2, 2, 3, 2, 0],
    },
    "Edebiyat": {
        "İslamiyet Öncesi": [1, 1, 1, 1, 1],
        "Halk Edebiyatı": [2, 2, 2, 2, 2],
        "Divan Edebiyatı": [4, 4, 5, 5, 3],
        "Tanzimat Edebiyatı": [2, 2, 1, 2, 2],
        "Servet-i Fünun": [1, 1, 1, 1, 1],
        "Milli Edebiyat": [1, 1, 1, 1, 1],
        "Cumhuriyet (Şiir & Roman)": [4, 4, 4, 4, 4],
        "Şiir Bilgisi": [3, 3, 3, 3, 2],
    }
}
