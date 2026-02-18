"""
OmniPDR – models/konu_verileri.py
====================================
YKS ve LGS müfredat konuları.
Her ders için konu listesi ve alt-konu detayları.
"""

from __future__ import annotations

from typing import Dict, List


# ──────────────────────────────────────────────
# YKS TYT Konuları
# ──────────────────────────────────────────────
TYT_KONULARI: Dict[str, List[str]] = {
    "Türkçe": [
        "Sözcükte Anlam", "Cümlede Anlam", "Paragraf (Ana Düşünce)",
        "Paragraf (Yardımcı Düşünce)", "Paragraf (Yapı)", "Ses Bilgisi",
        "Yazım Kuralları", "Noktalama İşaretleri", "Sözcük Türleri",
        "Cümle Bilgisi (Öğeler)", "Fiil Çekimleri", "Anlatım Bozukluğu",
    ],
    "Temel Matematik": [
        "Temel Kavramlar", "Sayı Basamakları", "Bölme-Bölünebilme",
        "EBOB-EKOK", "Rasyonel Sayılar", "Ondalık Sayılar",
        "Basit Eşitsizlikler", "Mutlak Değer", "Üslü Sayılar",
        "Köklü Sayılar", "Çarpanlara Ayırma", "Oran-Orantı",
        "Denklem Çözme", "Problemler (Sayı-Kesir)", "Problemler (Yaş)",
        "Problemler (İşçi-Havuz)", "Problemler (Hız-Yol)", "Yüzde-Faiz",
        "Kümeler", "Fonksiyonlar", "Permütasyon-Kombinasyon",
        "Olasılık", "İstatistik (Ortalama-Medyan)", "Veri Yorumlama",
    ],
    "Sosyal Bilimler": [
        "Tarih Bilimi", "İlk Çağ Uygarlıkları", "İlk Türk Devletleri",
        "İslam Tarihi", "Osmanlı Kuruluş", "Osmanlı Yükselme",
        "Coğrafya – Harita Bilgisi", "Coğrafya – İklim",
        "Coğrafya – Nüfus", "Coğrafya – Türkiye Fiziki",
        "Felsefe – Bilgi Felsefesi", "Felsefe – Ahlak Felsefesi",
        "Din – İbadetler", "Din – Hz. Muhammed'in Hayatı",
    ],
    "Fen Bilimleri": [
        "Fizik – Kuvvet ve Hareket", "Fizik – Enerji",
        "Fizik – Elektrik", "Fizik – Optik", "Fizik – Dalgalar",
        "Kimya – Atom ve Periyodik Tablo", "Kimya – Kimyasal Bağlar",
        "Kimya – Madde ve Özellikleri", "Kimya – Asit-Baz",
        "Biyoloji – Hücre", "Biyoloji – Canlıların Sınıflandırılması",
        "Biyoloji – Sistemler (Sindirim)", "Biyoloji – Ekosistem",
    ],
}


# ──────────────────────────────────────────────
# YKS AYT Konuları
# ──────────────────────────────────────────────
AYT_KONULARI: Dict[str, List[str]] = {
    "Matematik": [
        "Temel Kavramlar ve Sayılar", "Fonksiyonlar",
        "Polinomlar", "İkinci Dereceden Denklemler",
        "Eşitsizlikler", "Trigonometri", "Logaritma",
        "Diziler ve Seriler", "Limit", "Türev",
        "Türev Uygulamaları", "İntegral", "İntegral Uygulamaları",
        "Analitik Geometri", "Doğrunun Analitik İncelenmesi",
        "Çemberin Analitik İncelenmesi", "Konikler",
        "Uzay Geometri", "Katı Cisimler",
    ],
    "Fizik": [
        "Vektörler", "Kuvvet Dengesi", "Tork",
        "Düzgün Dairesel Hareket", "İş-Enerji-Güç",
        "İtme ve Momentum", "Elektrik Alan", "Manyetik Alan",
        "Elektromanyetik İndüksiyon", "Alternatif Akım",
        "Modern Fizik", "Atom Fiziği", "Radyoaktivite",
    ],
    "Kimya": [
        "Mol Kavramı", "Kimyasal Tepkimeler", "Termokimya",
        "Tepkime Hızı", "Kimyasal Denge", "Çözünürlük Dengesi",
        "Asitler ve Bazlar", "Elektrokimya",
        "Organik Kimya – Hidrokarbonlar", "Organik Kimya – Fonksiyonel Gruplar",
    ],
    "Biyoloji": [
        "Nükleik Asitler ve Protein Sentezi", "Enzimler",
        "Hücre Bölünmeleri", "Kalıtım (Genetik)", "Biyoteknoloji",
        "Canlıların Sınıflandırılması", "Bitki Biyolojisi",
        "Sinir Sistemi", "Endokrin Sistem", "Duyu Organları",
        "Komünite ve Popülasyon Ekolojisi",
    ],
    "Edebiyat": [
        "Şiir Bilgisi", "Edebi Akımlar", "Divan Edebiyatı",
        "Halk Edebiyatı", "Tanzimat Edebiyatı", "Servet-i Fünun",
        "Milli Edebiyat", "Cumhuriyet Dönemi (Şiir)",
        "Cumhuriyet Dönemi (Roman)", "Roman İnceleme",
    ],
    "Tarih-1": [
        "Osmanlı Duraklama", "Osmanlı Gerileme",
        "Osmanlı Dağılma", "I. Dünya Savaşı",
        "Mondros Mütarekesi", "Kurtuluş Savaşı Hazırlık",
        "Kurtuluş Savaşı Cepheleri", "Mudanya ve Lozan",
    ],
    "Coğrafya-1": [
        "Dünya'nın Şekli ve Hareketleri", "Harita Bilgisi",
        "İklim Bilgisi", "Hidrografya", "Toprak Coğrafyası", "Bitki Coğrafyası",
    ],
}


# ──────────────────────────────────────────────
# LGS Konuları (8. Sınıf Müfredatı)
# ──────────────────────────────────────────────
LGS_KONULARI: Dict[str, List[str]] = {
    "Türkçe": [
        "Sözcükte Anlam", "Cümlede Anlam", "Paragrafta Anlam",
        "Sözcük Türleri", "Cümle Türleri", "Fiilimsiler",
        "Anlatım Bozuklukları", "Yazım Kuralları", "Noktalama",
    ],
    "Matematik": [
        "Üslü İfadeler", "Kareköklü İfadeler", "Veri Analizi",
        "Basit Eşitsizlikler", "Cebirsel İfadeler – Çarpanlara Ayırma",
        "Doğrusal Denklemler", "Eşitsizlikler", "Üçgenler",
        "Eşlik ve Benzerlik", "Dönüşüm Geometrisi", "Geometrik Cisimler",
        "Olasılık",
    ],
    "Fen Bilimleri": [
        "Mevsimler ve İklim", "DNA ve Genetik Kod", "Basınç",
        "Madde ve Endüstri", "Basit Makineler", "Enerji Dönüşümleri",
        "Elektrik Yükleri", "Periyodik Sistem", "Kimyasal Tepkimeler",
    ],
    "T.C. İnkılap Tarihi": [
        "Bir Kahraman Doğuyor", "MKA'nın Askerlik Hayatı",
        "Milli Mücadele Hazırlık", "Cepheler", "Türk İnkılabı",
        "Atatürkçülük", "Atatürk Dönemi Türk Dış Politikası",
        "Atatürk'ün Ölümü ve Sonrası",
    ],
    "Din Kültürü": [
        "Kader İnancı", "Zekât ve Sadaka", "Din ve Hayat",
        "Hz. Muhammed'in Örnekliği", "Anadolu'da İslam",
    ],
    "İngilizce": [
        "Friendship", "Teen Life", "In The Kitchen",
        "On The Phone", "The Internet", "Adventures",
        "Tourism", "Chores", "Science", "Natural Forces",
    ],
}


def konu_listesi_getir(sinav_turu: str, ders: str) -> List[str]:
    """Sınav türü ve derse göre konu listesi döndürür."""
    if sinav_turu == "LGS":
        return LGS_KONULARI.get(ders, [])
    elif sinav_turu == "TYT":
        return TYT_KONULARI.get(ders, [])
    elif sinav_turu == "AYT":
        return AYT_KONULARI.get(ders, [])
    return []


def tum_dersler(sinav_turu: str) -> List[str]:
    """Sınav türüne göre tüm ders isimlerini döndürür."""
    if sinav_turu == "LGS":
        return list(LGS_KONULARI.keys())
    elif sinav_turu == "TYT":
        return list(TYT_KONULARI.keys())
    elif sinav_turu == "AYT":
        return list(AYT_KONULARI.keys())
    return []
