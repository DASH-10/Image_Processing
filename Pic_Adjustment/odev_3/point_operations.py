"""

Amaç:
Bu dosyada Soru 1 ve Soru 5'te istenen temel nokta işlemleri
(Parlaklık, Kontrast, Negatif, Eşikleme, Gamma düzeltmesi)
fonksiyonlar halinde tanımlanmıştır.
Tüm işlemler NumPy dizileri üzerinde manuel olarak yapılmıştır.
"""

import numpy as np

# -----------------------------------------------------------
# Yardımcı Fonksiyon
# -----------------------------------------------------------
def _to_uint8(arr: np.ndarray) -> np.ndarray:
    """
    Dizi değerlerini [0,255] aralığında sınırlar (clip eder)
    ve uint8 tipine dönüştürür.
    Bu adım taşma (overflow) ve taşma altı (underflow) hatalarını önler.
    """
    return np.clip(arr, 0, 255).astype(np.uint8)

# -----------------------------------------------------------
# 1a) Parlaklık Ayarlama
# -----------------------------------------------------------
def adjust_brightness(img: np.ndarray, value: int) -> np.ndarray:
    """
    Parlaklık ayarlama işlemi.
    Mantık: Her piksel değerine sabit bir sayı eklemek veya çıkarmak.

    Formül: out = in + value
    value > 0 → görüntü aydınlanır
    value < 0 → görüntü kararır
    """
    # int16 kullanıyoruz çünkü uint8 + value taşmaya sebep olabilir
    return _to_uint8(img.astype(np.int16) + int(value))

# -----------------------------------------------------------
# 1b) Kontrast Ayarlama
# -----------------------------------------------------------
def adjust_contrast(img: np.ndarray, factor: float) -> np.ndarray:
    """
    Kontrast değişimi 128 (orta gri) etrafında yapılır.
    Piksel değerleri 128'e göre uzaklaştırılarak veya yaklaştırılarak ölçeklenir.

    Formül: out = factor * (in - 128) + 128
    factor > 1  → kontrast artar (renkler daha belirgin)
    factor < 1  → kontrast azalır (renkler birbirine yaklaşır)
    """
    return _to_uint8(factor * (img.astype(np.float32) - 128.0) + 128.0)

# -----------------------------------------------------------
# 1c) Negatif Görüntü
# -----------------------------------------------------------
def image_negative(img: np.ndarray) -> np.ndarray:
    """
    Negatif dönüşüm:
    Tüm parlaklık değerleri ters çevrilir.
    Karanlık alanlar aydınlanır, aydınlık alanlar kararır.

    Formül: out = 255 - in
    """
    return _to_uint8(255 - img.astype(np.int16))

# -----------------------------------------------------------
# 1d) Eşikleme (Thresholding)
# -----------------------------------------------------------
def threshold(img: np.ndarray, T: int) -> np.ndarray:
    """
    Basit ikili eşikleme işlemi.
    Eğer piksel değeri T'den büyükse 255 (beyaz), küçükse 0 (siyah) yapılır.

    Örnek:
      T = 120 → 120 üzeri beyaz, altı siyah.
    """
    return (img > int(T)).astype(np.uint8) * 255

# -----------------------------------------------------------
# 5) Gamma Düzeltmesi
# -----------------------------------------------------------
def gamma_correction(img: np.ndarray, gamma: float) -> np.ndarray:
    """
    Gamma düzeltmesi (nonlineer ton ayarlama).
    Görselin genel parlaklık dengesini değiştirir.

    Formül: out = 255 * (in / 255) ^ gamma

    γ < 1  → koyu alanları aydınlatır
    γ > 1  → parlak alanları bastırır
    γ = 1  → görüntü değişmez
    """
    # Piksel değerlerini 0-1 aralığına indiriyoruz
    x = img.astype(np.float32) / 255.0
    # Gamma fonksiyonu uygulanır
    y = np.power(x, float(gamma))
    # Tekrar 0-255 aralığına çıkarılır
    return _to_uint8(y * 255.0)
