"""
Not:
- Tüm ağır iş (parlaklık/kontrast/negatif/threshold/gamma, histogram,
  kontrast germe ve histogram eşitleme) ayrı modüllerde yazıldı.
- Buradaki kod sadece "orkestra şefi" gibi davranır: yükler, çağırır, kaydeder.
"""

import os
from pathlib import Path
import numpy as np
import cv2
import matplotlib.pyplot as plt

# --- Kendi fonksiyonlarımızı içe aktaralım (ayrı dosyalara yazdım) ---
from point_operations import (
    adjust_brightness, adjust_contrast, image_negative, threshold, gamma_correction
)
from histogram_processing import (
    compute_histogram, image_stats, contrast_stretch, hist_equalize
)

# --- Klasör kurulumları ---
BASE = Path(__file__).resolve().parent             # projenin bulunduğu klasör
IMG_DIR = BASE / "test_images"                     # giriş görselleri
OUT_DIR = BASE / "results"                         # tüm çıktılar buraya düşer
OUT_DIR.mkdir(parents=True, exist_ok=True)         # yoksa oluştur

# --- Bu ödevde kullanacağımız DÖRT görüntünün kesin isimleri ---
# (dosya adları birebir böyle olmalı; yoksa cv2.imread None döndürür)
TEST_IMAGES = [
    "inggrid-koe-kbKEuU-YEIw-unsplash.jpg",          # foggy forest (low-contrast)
    "michael-tomlinson-ih2JHLPy6vg-unsplash.jpg",    # bridge B&W (high-contrast)
    "vladut-anton-Q0GHqEaHEhA-unsplash.jpg",         # bright field (overexposed)
    "yiran-ding-IrGyuTSrkK4-unsplash.jpg",           # night street (dark)
]

def load_gray(path: Path, size=(256, 256)):
    """
    Bir görüntüyü GRAYSCALE olarak okur ve (isteğe bağlı) ortak boyuta getirir.
    Neden? Tüm işlemleri adil kıyaslamak ve çıktı boyutlarını sabit tutmak için.

    Parametreler:
      path : görüntü dosyasının yolu
      size : (genişlik, yükseklik) -> None verirsek yeniden boyutlanmaz

    Dönüş:
      img  : uint8, 0–255 aralığında, tek kanallı görüntü
    """
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        # Burada hata vermek iyi; sessizce devam edersek neyin yanlış gittiğini bulmak zorlaşır.
        raise FileNotFoundError(f"Cannot open: {path}")
    if size is not None:
        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return img

def save_img(name: str, img: np.ndarray) -> Path:
    """
    Görseli results/ klasörüne kaydeder ve yolunu döndürür.
    """
    p = OUT_DIR / name
    cv2.imwrite(str(p), img)
    return p

def save_hist(name: str, img: np.ndarray) -> Path:
    """
    Görüntünün histogramını (manuel hist ile) çizer ve PNG olarak kaydeder.
    Neden manuel hist? Ödev gereği histogram hesaplamasını kendimiz yaptık.
    """
    hist = compute_histogram(img)
    plt.figure()
    plt.title(name)
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")
    plt.bar(np.arange(256), hist)  # 0..255 binleri
    plt.tight_layout()
    p = OUT_DIR / f"{name}_hist.png"
    plt.savefig(p)
    plt.close()
    return p

def show_2x2(tag: str, A: np.ndarray, B: np.ndarray, titleA: str, titleB: str) -> Path:
    """
    2x2 kıyas çizimi: Üstte görüntüler, altta her birinin histogramı.
    Rapor için tek görselde hem çıktı hem de dağılımı beraber sunmak çok pratik.
    """
    fig, axs = plt.subplots(2, 2, figsize=(8, 6))

    # ÜST SATIR: görüntüler
    axs[0, 0].imshow(A, cmap="gray", vmin=0, vmax=255)
    axs[0, 0].set_title(titleA)
    axs[0, 0].axis("off")

    axs[0, 1].imshow(B, cmap="gray", vmin=0, vmax=255)
    axs[0, 1].set_title(titleB)
    axs[0, 1].axis("off")

    # ALT SATIR: histogramlar (manuel hist fonksiyonu)
    ha = compute_histogram(A)
    hb = compute_histogram(B)
    axs[1, 0].bar(np.arange(256), ha)
    axs[1, 0].set_title(f"{titleA} Histogram")
    axs[1, 0].set_xlabel("Intensity")
    axs[1, 0].set_ylabel("Frequency")

    axs[1, 1].bar(np.arange(256), hb)
    axs[1, 1].set_title(f"{titleB} Histogram")
    axs[1, 1].set_xlabel("Intensity")

    fig.tight_layout()
    out = OUT_DIR / f"{tag}_2x2.png"
    fig.savefig(out)
    plt.close(fig)
    return out

# --------------------------------------------------------------------
# SORULAR (her biri ayrı küçük "pipeline" gibi)
# --------------------------------------------------------------------

def run_q1_point_ops(img: np.ndarray, stem: str) -> None:
    """
    Soru 1 – Temel Nokta İşlemleri:
      - Parlaklık: ±40
      - Kontrast : ×1.5 ve ×0.7 (128 etrafında)
      - Negatif  : 255 - p
      - Threshold: T = medyan (basit ve otomatik bir seçim)
    """
    # Parlaklık
    save_img(f"{stem}_bright_plus.jpg", adjust_brightness(img, +40))
    save_img(f"{stem}_bright_minus.jpg", adjust_brightness(img, -40))

    # Kontrast (daha sert ve daha yumuşak)
    save_img(f"{stem}_contrast_1_5.jpg", adjust_contrast(img, 1.5))
    save_img(f"{stem}_contrast_0_7.jpg", adjust_contrast(img, 0.7))

    # Negatif
    save_img(f"{stem}_negative.jpg", image_negative(img))

    # Threshold (medyandan daha büyük olanları beyaz yap)
    T = int(np.percentile(img, 50))  # median ~= %50 persentil
    save_img(f"{stem}_thresh_{T}.jpg", threshold(img, T))

def run_q2_hist_and_stats(img: np.ndarray, stem: str) -> None:
    """
    Soru 2 – Histogram ve İstatistikler:
      - Histogram grafiği PNG olarak kaydedilir.
      - mean, std, entropy, min, max -> TXT dosyası olarak kaydedilir.
    """
    save_hist(f"{stem}_orig", img)
    stats = image_stats(img)
    with open(OUT_DIR / f"{stem}_stats.txt", "w", encoding="utf-8") as f:
        for k, v in stats.items():
            f.write(f"{k}: {v}\n")

def run_q3_contrast_stretch(img: np.ndarray, stem: str) -> None:
    """
    Soru 3 – Kontrast Germe:
      - Dinamik aralığı [min, max] -> [0, 255] ölçekle.
      - Hem çıktı görselini hem de 2x2 kıyası kaydet.
    """
    stretched = contrast_stretch(img)
    save_img(f"{stem}_stretched.jpg", stretched)
    show_2x2(f"{stem}_stretch", img, stretched, "Original", "Contrast Stretched")

def run_q4_hist_eq(img: np.ndarray, stem: str) -> None:
    """
    Soru 4 – Histogram Eşitleme:
      - CDF tabanlı LUT ile piksel değerlerini yeniden dağıt.
      - 2x2 kıyas görseli de üret.
    """
    heq = hist_equalize(img)
    save_img(f"{stem}_histeq.jpg", heq)
    show_2x2(f"{stem}_histeq", img, heq, "Original", "Hist. Equalized")

def run_q5_gamma(img: np.ndarray, stem: str) -> None:
    """
    Soru 5 – Gamma Düzeltmesi:
      - Farklı gamma değerlerinin (0.5, 1.0, 1.5, 2.0, 2.5) çıktılarını kaydet.
      - γ < 1 -> karanlık bölgeler açılır; γ > 1 -> parlak bölgeler bastırılır.
    """
    for g in [0.5, 1.0, 1.5, 2.0, 2.5]:
        save_img(f"{stem}_gamma_{str(g).replace('.', '_')}.jpg", gamma_correction(img, g))

# --------------------------------------------------------------------
# ANA AKIŞ
# --------------------------------------------------------------------

def main() -> None:
    """
    Her görüntü için:
      1) Yükle (grayscale + 256x256)
      2) Orijinali kaydet
      3) Soru 1–5 fonksiyonlarını sırayla çalıştır
      4) Konsola kısa durum mesajı yaz
    """
    print("=== Görüntü İşleme 3 – Runner ===")
    for fname in TEST_IMAGES:
        path = IMG_DIR / fname
        img = load_gray(path)                     # grayscale 256×256
        stem = Path(fname).stem
        save_img(f"{stem}_gray.jpg", img)         # referans olarak orijinali kaydet

        # Ödevde istenen beş bölüm:
        run_q1_point_ops(img, stem)               # Soru 1
        run_q2_hist_and_stats(img, stem)          # Soru 2
        run_q3_contrast_stretch(img, stem)        # Soru 3
        run_q4_hist_eq(img, stem)                 # Soru 4
        run_q5_gamma(img, stem)                   # Soru 5

        print(f"Processed: {fname}")

    print(f"All outputs saved in: {OUT_DIR}")

if __name__ == "__main__":
    main()
