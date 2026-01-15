"""
Amaç:
Bu dosyada histogram ve istatistik temelli işlemler (Soru 2, 3 ve 4)
yer alıyor. Tüm işlemler sıfırdan, NumPy kullanılarak manuel biçimde yapılmıştır.
"""

import numpy as np

# -----------------------------------------------------------
# 2a) Histogram Hesaplama
# -----------------------------------------------------------
def compute_histogram(img: np.ndarray) -> np.ndarray:
    """
    Gri-seviye bir görüntünün histogramını manuel olarak hesaplar.

    Mantık:
      - 0–255 aralığında 256 olasılık vardır.
      - Her pikselin yoğunluk değerine göre sayım yapılır.

    Dönüş:
      hist : Uzunluğu 256 olan bir dizi (her bin = kaç piksel var)
    """
    hist = np.zeros(256, dtype=np.int64)  # 256 olası gri seviye
    for v in img.ravel():                 # görüntüyü 1D vektör gibi düşün
        hist[int(v)] += 1                 # her değerin sıklığını say
    return hist

# -----------------------------------------------------------
# 2b) Görüntü İstatistikleri
# -----------------------------------------------------------
def image_stats(img: np.ndarray) -> dict:
    """
    Bir görüntü için temel istatistikleri döndürür:
      - Ortalama (mean)
      - Standart sapma (std)
      - Entropi (bilgi miktarı)
      - Minimum ve maksimum değerler

    Entropi, olasılık dağılımı p ile hesaplanır:
      entropy = -Σ(p * log2(p)), p>0 olan değerler için
    """
    hist = compute_histogram(img)         # önce histogramı al
    N = img.size                          # toplam piksel sayısı
    p = hist / float(N)                   # PDF (olasılık dağılımı)
    nz = p[p > 0]                         # 0 olanları çıkar (log2(0) tanımsız)
    entropy = -np.sum(nz * np.log2(nz))   # entropi formülü

    # Sözlük olarak döndür (kolay erişim için)
    return dict(
        mean=float(np.mean(img)),
        std=float(np.std(img)),
        entropy=float(entropy),
        min=int(np.min(img)),
        max=int(np.max(img)),
    )

# -----------------------------------------------------------
# 3) Kontrast Germe (Contrast Stretching)
# -----------------------------------------------------------
def contrast_stretch(img: np.ndarray) -> np.ndarray:
    """
    Kontrast Germe işlemi:
    Piksel değerlerini [min, max] aralığından [0, 255] aralığına yeniden ölçekler.

    Formül:
      out = (in - min) / (max - min) * 255

    Amaç:
      - Düşük kontrastlı görüntüleri genişletip daha net hale getirmek.
      - Eğer min ve max eşitse (düz görüntü), sıfır matris döndürür.
    """
    lo = float(np.min(img))
    hi = float(np.max(img))
    if hi == lo:
        # Tüm pikseller aynıysa kontrast germe yapılamaz
        return np.zeros_like(img, dtype=np.uint8)

    # Germe işlemi (float32 kullanılmazsa precision kaybı olabilir)
    out = (img.astype(np.float32) - lo) / (hi - lo) * 255.0
    return out.astype(np.uint8)

# -----------------------------------------------------------
# 4) Histogram Eşitleme (Histogram Equalization)
# -----------------------------------------------------------
def hist_equalize(img: np.ndarray) -> np.ndarray:
    """
    Histogram Eşitleme işlemi (manuel implementasyon).

    Adımlar:
      1. Histogramı hesapla.
      2. Olasılık yoğunluk fonksiyonu (pdf) oluştur: hist / N
      3. Kümülatif dağılım fonksiyonu (cdf) hesapla: np.cumsum(pdf)
      4. Yeni değerleri belirle: LUT = floor(255 * cdf)
      5. Her pikseli LUT tablosu ile dönüştür.

    Sonuç:
      - Karanlık ve aydınlık tonlar daha dengeli dağılır.
      - Görüntü genel olarak daha kontrastlı görünür.
    """
    hist = compute_histogram(img)
    pdf = hist / float(img.size)              # Olasılık dağılımı
    cdf = np.cumsum(pdf)                      # Kümülatif dağılım fonksiyonu
    lut = np.floor(255 * cdf).astype(np.uint8) # Look-Up Table (0–255 dönüşümü)
    return lut[img]                           # Her pikseli yeni değere eşleştir
