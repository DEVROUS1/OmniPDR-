"""
OmniPDR – models/ogrenci_sinifi.py
=====================================
Veri modelleri ve OOP sınıfları.

Psikolojik Temel:
  - Zimmerman'ın Öz-Düzenlemeli Öğrenmesi: Öğrenci yalnızca akademik
    değil; uyku, stres ve çalışma saati gibi bütünsel verilerle takip edilir.
  - Ebbinghaus'un Aralıklı Tekrarı: Her hata kaydı, tekrar takvimi
    üretecek metadata ile saklanır.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


# ──────────────────────────────────────────────
# 1. YKS/LGS Ders Adları (sabit değerler)
# ──────────────────────────────────────────────
DERSLER_YKS = ["Türkçe", "Matematik", "Fizik", "Kimya", "Biyoloji",
               "Tarih", "Coğrafya", "Felsefe", "Din", "Yabancı Dil"]
DERSLER_LGS = ["Türkçe", "Matematik", "Fen Bilimleri",
               "T.C. İnkılap Tarihi", "Din Kültürü", "İngilizce"]


# ──────────────────────────────────────────────
# 2. GörüşmeNotu – Tarih damgalı PDR notları
# ──────────────────────────────────────────────
@dataclass
class GorusmeNotu:
    """
    Tek bir psikolojik danışma görüşmesini temsil eder.
    Her not; tarih, içerik ve danışmanın kısa değerlendirmesini içerir.
    """
    tarih: date
    icerik: str
    degerlendirme: Optional[str] = None  # Danışman yorumu
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tarih": self.tarih.isoformat(),
            "icerik": self.icerik,
            "degerlendirme": self.degerlendirme,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GorusmeNotu":
        return cls(
            tarih=date.fromisoformat(d["tarih"]),
            icerik=d["icerik"],
            degerlendirme=d.get("degerlendirme"),
            id=d.get("id", str(uuid.uuid4())[:8]),
        )


# ──────────────────────────────────────────────
# 3. HataKaydi – Ebbinghaus aralıklı tekrar birimi
# ──────────────────────────────────────────────
@dataclass
class HataKaydi:
    """
    Bir öğrencinin yanlış yaptığı tek bir konuyu/soruyu temsil eder.
    Ebbinghaus'un eğrisine göre tekrar tarihleri otomatik hesaplanır:
      → 1., 3., 7., 21. ve 30. günler.
    """
    ders: str
    konu: str
    hata_tarihi: date
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    # Tekrar tarihleri algoritma tarafından doldurulur
    tekrar_tarihleri: List[date] = field(default_factory=list)
    tamamlanan_tekrarlar: List[date] = field(default_factory=list)

    # Ebbinghaus aralık gün sayıları
    ARALIK_GUNLER: tuple = field(default=(1, 3, 7, 21, 30), init=False, repr=False)

    def __post_init__(self):
        if not self.tekrar_tarihleri:
            self._tekrar_takvimi_olustur()

    def _tekrar_takvimi_olustur(self):
        """Hata tarihinden itibaren 5 tekrar günü hesaplar."""
        from datetime import timedelta
        self.tekrar_tarihleri = [
            self.hata_tarihi + timedelta(days=g)
            for g in self.ARALIK_GUNLER
        ]

    @property
    def bugunun_tekrari_var_mi(self) -> bool:
        """Bugün herhangi bir planlı tekrar günü mü?"""
        bugun = date.today()
        return any(
            t == bugun and t not in self.tamamlanan_tekrarlar
            for t in self.tekrar_tarihleri
        )

    @property
    def bekleyen_tekrar_sayisi(self) -> int:
        """Henüz tamamlanmamış, tarihi geçmiş veya bugünkü tekrarlar."""
        bugun = date.today()
        return sum(
            1 for t in self.tekrar_tarihleri
            if t <= bugun and t not in self.tamamlanan_tekrarlar
        )

    def tekrar_tamamla(self, tarih: Optional[date] = None):
        """Bir tekrar seansını tamamlandı olarak işaretle."""
        tarih = tarih or date.today()
        if tarih not in self.tamamlanan_tekrarlar:
            self.tamamlanan_tekrarlar.append(tarih)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ders": self.ders,
            "konu": self.konu,
            "hata_tarihi": self.hata_tarihi.isoformat(),
            "tekrar_tarihleri": [t.isoformat() for t in self.tekrar_tarihleri],
            "tamamlanan_tekrarlar": [t.isoformat() for t in self.tamamlanan_tekrarlar],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "HataKaydi":
        obj = cls(
            ders=d["ders"],
            konu=d["konu"],
            hata_tarihi=date.fromisoformat(d["hata_tarihi"]),
            id=d.get("id", str(uuid.uuid4())[:8]),
        )
        obj.tekrar_tarihleri = [date.fromisoformat(t) for t in d.get("tekrar_tarihleri", [])]
        obj.tamamlanan_tekrarlar = [date.fromisoformat(t) for t in d.get("tamamlanan_tekrarlar", [])]
        return obj


# ──────────────────────────────────────────────
# 4. DenemeKaydi – Haftalık sınav verisi
# ──────────────────────────────────────────────
@dataclass
class DenemeKaydi:
    """
    Bir deneme sınavının tüm verilerini barındırır.
    Akademik performans + bütünsel (uyku, stres, çalışma) verisi bir arada.
    """
    tarih: date
    netleri: dict          # {"Türkçe": 28.5, "Matematik": 22.0, ...}
    calisma_saati: float   # O haftaki toplam çalışma saati
    stres_puani: int       # 1–10 arası öznel stres skoru
    uyku_saati: float      # Günlük ortalama uyku süresi (saat)
    notlar: str = ""       # Serbest metin notlar

    @property
    def toplam_net(self) -> float:
        return sum(self.netleri.values())

    def to_dict(self) -> dict:
        return {
            "tarih": self.tarih.isoformat(),
            "netleri": self.netleri,
            "calisma_saati": self.calisma_saati,
            "stres_puani": self.stres_puani,
            "uyku_saati": self.uyku_saati,
            "notlar": self.notlar,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DenemeKaydi":
        return cls(
            tarih=date.fromisoformat(d["tarih"]),
            netleri=d["netleri"],
            calisma_saati=d["calisma_saati"],
            stres_puani=d["stres_puani"],
            uyku_saati=d.get("uyku_saati", 7.0),
            notlar=d.get("notlar", ""),
        )


# ──────────────────────────────────────────────
# 5. Ogrenci – Ana domain sınıfı
# ──────────────────────────────────────────────
class Ogrenci:
    """
    Sistemdeki her öğrenciyi temsil eden merkezi sınıf.
    CRM, akademik performans ve PDR notlarını tek noktada toplar.
    """

    def __init__(
        self,
        ad: str,
        hedef_bolum: str,
        sinav_turu: str = "YKS",   # "YKS" veya "LGS"
        hedef_net: Optional[float] = None,
        ogrenci_id: Optional[str] = None,
    ):
        self.ogrenci_id: str = ogrenci_id or str(uuid.uuid4())[:12]
        self.ad: str = ad
        self.hedef_bolum: str = hedef_bolum
        self.sinav_turu: str = sinav_turu
        self.hedef_net: Optional[float] = hedef_net
        self.kayit_tarihi: date = date.today()

        # Alt koleksiyonlar
        self.deneme_kayitlari: List[DenemeKaydi] = []
        self.hata_kayitlari: List[HataKaydi] = []
        self.gorusme_notlari: List[GorusmeNotu] = []

    # ── Veri ekleme yardımcıları ──────────────────

    def deneme_ekle(self, kayit: DenemeKaydi) -> None:
        """Yeni bir deneme kaydı ekler (tarihe göre sıralı tutar)."""
        self.deneme_kayitlari.append(kayit)
        self.deneme_kayitlari.sort(key=lambda d: d.tarih)

    def hata_ekle(self, ders: str, konu: str, tarih: Optional[date] = None) -> HataKaydi:
        """
        Yeni bir konu hatası ekler ve otomatik olarak Ebbinghaus
        takvimi oluşturur.
        """
        kayit = HataKaydi(ders=ders, konu=konu, hata_tarihi=tarih or date.today())
        self.hata_kayitlari.append(kayit)
        return kayit

    def gorusme_ekle(self, icerik: str, degerlendirme: Optional[str] = None) -> GorusmeNotu:
        """Yeni bir PDR görüşme notu ekler."""
        not_ = GorusmeNotu(
            tarih=date.today(),
            icerik=icerik,
            degerlendirme=degerlendirme,
        )
        self.gorusme_notlari.append(not_)
        return not_

    # ── Hesaplama özellikleri ──────────────────

    @property
    def son_deneme(self) -> Optional[DenemeKaydi]:
        return self.deneme_kayitlari[-1] if self.deneme_kayitlari else None

    @property
    def bugunun_tekrar_listesi(self) -> List[HataKaydi]:
        """Bugün tekrar edilmesi gereken konular."""
        return [h for h in self.hata_kayitlari if h.bugunun_tekrari_var_mi]

    @property
    def bekleyen_tekrar_sayisi(self) -> int:
        return sum(h.bekleyen_tekrar_sayisi for h in self.hata_kayitlari)

    @property
    def dersler(self) -> List[str]:
        """Sınav türüne göre ders listesi."""
        return DERSLER_YKS if self.sinav_turu == "YKS" else DERSLER_LGS

    # ── Serileştirme ──────────────────────────

    def to_dict(self) -> dict:
        return {
            "ogrenci_id": self.ogrenci_id,
            "ad": self.ad,
            "hedef_bolum": self.hedef_bolum,
            "sinav_turu": self.sinav_turu,
            "hedef_net": self.hedef_net,
            "kayit_tarihi": self.kayit_tarihi.isoformat(),
            "deneme_kayitlari": [d.to_dict() for d in self.deneme_kayitlari],
            "hata_kayitlari": [h.to_dict() for h in self.hata_kayitlari],
            "gorusme_notlari": [g.to_dict() for g in self.gorusme_notlari],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Ogrenci":
        ogr = cls(
            ad=d["ad"],
            hedef_bolum=d["hedef_bolum"],
            sinav_turu=d.get("sinav_turu", "YKS"),
            hedef_net=d.get("hedef_net"),
            ogrenci_id=d.get("ogrenci_id"),
        )
        ogr.kayit_tarihi = date.fromisoformat(d.get("kayit_tarihi", date.today().isoformat()))
        ogr.deneme_kayitlari = [DenemeKaydi.from_dict(x) for x in d.get("deneme_kayitlari", [])]
        ogr.hata_kayitlari = [HataKaydi.from_dict(x) for x in d.get("hata_kayitlari", [])]
        ogr.gorusme_notlari = [GorusmeNotu.from_dict(x) for x in d.get("gorusme_notlari", [])]
        return ogr

    def __repr__(self) -> str:
        return f"<Ogrenci '{self.ad}' | {self.sinav_turu} | {len(self.deneme_kayitlari)} deneme>"
