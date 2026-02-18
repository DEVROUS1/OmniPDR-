"""
OmniPDR – models/soru_dagilimi.py
===================================
TYT ve AYT derslerine ait son 5 yılın (2019-2023) konu bazlı soru dağılımı verileri.
Veriler, çeşitli eğitim portalları ve ÖSYM istatistiklerinden derlenmiştir.
"""

from typing import Dict, List

# Yıllar sütunu: 2023, 2022, 2021, 2020, 2019
YILLAR = ["2023", "2022", "2021", "2020", "2019"]

TYT_DAGILIM: Dict[str, Dict[str, List[int]]] = {
    "Türkçe": {
        "Paragraf": [26, 26, 25, 26, 22],
        "Cümlede Anlam": [4, 3, 3, 6, 3],
        "Sözcükte Anlam": [3, 4, 5, 1, 3],
        "Dil Bilgisi (Karma)": [2, 3, 2, 3, 8],
        "Yazım Kuralları": [2, 2, 2, 2, 2],
        "Noktalama İşaretleri": [2, 2, 2, 2, 1],
        "Ses Bilgisi": [1, 0, 1, 0, 1],
    },
    "Temel Matematik": {
        "Problemler": [13, 13, 13, 13, 13],
        "Temel Kavramlar": [1, 2, 3, 1, 4],
        "Sayı Basamakları": [2, 0, 0, 3, 0],
        "Mutlak Değer": [1, 0, 0, 1, 1],
        "Üslü Sayılar": [1, 0, 1, 1, 0],
        "Fonksiyonlar": [1, 1, 1, 1, 1],
        "Kümeler": [1, 1, 1, 2, 1],
        "Olasılık & PKOB": [2, 2, 2, 2, 2],
        "Geometri": [10, 10, 10, 10, 10],
    },
    "Fizik": {
        "Optik": [1, 1, 1, 1, 2],
        "Isı ve Sıcaklık": [1, 1, 1, 1, 1],
        "Elektrik ve Manyetizma": [1, 1, 1, 1, 1],
        "Hareket ve Kuvvet": [1, 1, 1, 1, 1],
        "Madde ve Özellikleri": [1, 1, 1, 0, 1],
        "Basınç ve Kaldırma": [1, 1, 1, 1, 0],
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
        "Canlıların Ortak Özellikleri": [1, 1, 1, 0, 1],
        "Hücre": [1, 1, 1, 1, 1],
        "Canlıların Sınıflandırılması": [1, 1, 1, 1, 1],
        "Hücre Bölünmeleri": [1, 1, 1, 1, 1],
        "Kalıtım": [1, 1, 1, 1, 1],
        "Ekosistem Ekolojisi": [1, 1, 1, 1, 1],
    }
}

AYT_DAGILIM: Dict[str, Dict[str, List[int]]] = {
    "Matematik": {
        "Trigonometri": [4, 4, 4, 4, 4],
        "Türev": [3, 3, 3, 0, 4],
        "İntegral": [3, 3, 3, 0, 4],
        "Limit": [2, 2, 2, 0, 2],
        "Logaritma": [2, 2, 2, 2, 2],
        "Diziler": [1, 1, 1, 1, 1],
        "Fonksiyonlar": [2, 2, 2, 2, 2],
        "Polinomlar": [1, 1, 1, 1, 1],
        "Parabol": [1, 1, 1, 1, 1],
        "Geometri": [10, 10, 10, 10, 10],
    },
    "Fizik": {
        "Çembersel Hareket": [2, 2, 2, 2, 2],
        "Basit Harmonik Hareket": [1, 1, 1, 1, 1],
        "İtme ve Momentum": [1, 1, 1, 1, 1],
        "Elektrik Alan ve Potansiyel": [2, 2, 2, 2, 2],
        "Manyetizma ve İndüksiyon": [2, 2, 2, 2, 2],
        "Modern Fizik": [2, 2, 2, 0, 2],
        "Atom Fiziği": [1, 1, 1, 0, 1],
        "Fotoelektrik & Compton": [1, 1, 1, 0, 1],
    },
    "Kimya": {
        "Modern Atom Teorisi": [1, 1, 1, 1, 1],
        "Gazlar": [1, 1, 1, 1, 1],
        "Sıvı Çözeltiler": [2, 1, 1, 1, 1],
        "Kimyasal Enerji": [1, 1, 1, 1, 1],
        "Kimyasal Hız": [1, 1, 1, 1, 1],
        "Kimyasal Denge": [1, 1, 1, 1, 1],
        "Asit-Baz Dengesi": [1, 1, 1, 1, 1],
        "Elektrokimya": [2, 2, 2, 1, 2],
        "Organik Kimya": [3, 3, 3, 0, 4],
    },
    "Biyoloji": {
        "Sinir Sistemi": [1, 1, 1, 1, 1],
        "Endokrin Sistem": [1, 1, 1, 1, 1],
        "Duyu Organları": [1, 1, 1, 1, 1],
        "Destek ve Hareket": [1, 0, 0, 1, 1],
        "Dolaşım Sistemi": [1, 1, 1, 1, 1],
        "Solunum Sistemi": [1, 1, 1, 1, 1],
        "Protein Sentezi": [2, 2, 2, 1, 2],
        "Fotosentez/Kemosentez": [1, 1, 1, 1, 1],
        "Hücre Solunumu": [1, 1, 1, 1, 1],
        "Bitki Biyolojisi": [2, 3, 2, 0, 2],
    }
}
