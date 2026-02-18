"""
OmniPDR – core/veritabani.py
================================
JSON tabanlı kalıcılık katmanı.

Tasarım kararı: Üretim ortamında bu katman SQLite/PostgreSQL
ile kolayca değiştirilebilir. Repository pattern uygulanmıştır;
böylece Streamlit kodu doğrudan dosya/DB detaylarından bağımsızdır.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from models.ogrenci_sinifi import Ogrenci


# ──────────────────────────────────────────────
# Veritabanı Yolu
# ──────────────────────────────────────────────
_VARSAYILAN_YOL = Path(__file__).parent.parent / "data" / "ogrenciler.json"


class OgrenciRepository:
    """
    Tüm öğrenci verilerini JSON dosyasında saklayan ve yöneten sınıf.

    Kullanım:
        repo = OgrenciRepository()
        repo.kaydet(ogrenci)
        ogr = repo.getir_id_ile("abc123")
        hepsi = repo.hepsini_getir()
    """

    def __init__(self, dosya_yolu: Path = _VARSAYILAN_YOL):
        self.dosya_yolu = dosya_yolu
        self._bellek: Dict[str, Ogrenci] = {}  # id → Ogrenci
        self._yukle()

    # ── Dahili I/O ─────────────────────────────

    def _yukle(self) -> None:
        """JSON dosyasından tüm öğrencileri belleğe yükler."""
        if not self.dosya_yolu.exists():
            self.dosya_yolu.parent.mkdir(parents=True, exist_ok=True)
            self._kaydet_dosya()
            return

        with open(self.dosya_yolu, "r", encoding="utf-8") as f:
            ham = json.load(f)

        for ogr_dict in ham.get("ogrenciler", []):
            ogr = Ogrenci.from_dict(ogr_dict)
            self._bellek[ogr.ogrenci_id] = ogr

    def _kaydet_dosya(self) -> None:
        """Belleği JSON dosyasına yazar (atomic write ile veri kaybı önlenir)."""
        veri = {"ogrenciler": [ogr.to_dict() for ogr in self._bellek.values()]}
        tmp_yol = self.dosya_yolu.with_suffix(".tmp")
        with open(tmp_yol, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)
        os.replace(tmp_yol, self.dosya_yolu)  # Atomic rename

    # ── Genel CRUD operasyonları ───────────────

    def kaydet(self, ogrenci: Ogrenci) -> None:
        """Yeni veya mevcut öğrenciyi kaydeder/günceller."""
        self._bellek[ogrenci.ogrenci_id] = ogrenci
        self._kaydet_dosya()

    def getir_id_ile(self, ogrenci_id: str) -> Optional[Ogrenci]:
        return self._bellek.get(ogrenci_id)

    def getir_ad_ile(self, ad: str) -> Optional[Ogrenci]:
        for ogr in self._bellek.values():
            if ogr.ad.lower() == ad.lower():
                return ogr
        return None

    def hepsini_getir(self) -> List[Ogrenci]:
        return list(self._bellek.values())

    def sil(self, ogrenci_id: str) -> bool:
        if ogrenci_id in self._bellek:
            del self._bellek[ogrenci_id]
            self._kaydet_dosya()
            return True
        return False

    @property
    def toplam_ogrenci(self) -> int:
        return len(self._bellek)

    def __repr__(self) -> str:
        return f"<OgrenciRepository: {self.toplam_ogrenci} öğrenci | '{self.dosya_yolu}'>"
