# Görüntü İşleme 3. Ödevi – **Nokta İşlemleri ve Histogram İşleme**

**Öğrenci:** Omar A.M. Issa  

**Öğrenci No:** 220212901  

**Ders:** Görüntü İşleme (Yapay Zeka Mühendisliği)  

**Öğr. Üyesi:** Dr. Öğr. Üyesi Ramin Abbaszadi

---

## 1) Giriş ve Amaç

Bu ödevde bir gri-seviye görüntü üzerinde **nokta işlemleri** ve **histogram tabanlı** teknikler **sıfırdan** uygulanmıştır. Hazır fonksiyonlar (örn. `cv2.equalizeHist`, `cv2.calcHist`) **kullanılmamıştır**. Tüm işlemler **NumPy** dizileri ile gerçekleştirilmiş; görselleştirmeler **Matplotlib** ile yapılmıştır.

**Hedefler:**

- Temel nokta işlemlerini (parlaklık, kontrast, negatif, eşikleme) uygulamak
- Histogramı **elle** hesaplamak ve istatistikleri çıkarmak (mean, std, entropy, min, max)
- **Kontrast germe** ve **histogram eşitleme** algoritmalarını manuel uygulamak
- **Gamma düzeltmesi** ile farklı gamma değerlerinin etkisini incelemek
- Sonuçları dosya sistemine düzenli bir şekilde kaydetmek

---

## 2) Proje Yapısı

```
odev3/
 ├── main.py                         # Çalıştırılabilir ana betik
 ├── point_operations.py             # Soru 1 ve 5 fonksiyonları (parlaklık, kontrast, negatif, eşikleme, gamma)
 ├── histogram_processing.py         # Soru 2–4 fonksiyonları (histogram, istatistik, germe, eşitleme)
 ├── test_images/                    # Test görselleri (Unsplash)
 │    ├── inggrid-koe-kbKEuU-YEIw-unsplash.jpg   # Foggy forest (low-contrast)
 │    ├── michael-tomlinson-ih2JHLPy6vg-unsplash.jpg  # Bridge B&W (high-contrast)
 │    ├── vladut-anton-Q0GHqEaHEhA-unsplash.jpg       # Bright field (overexposed)
 │    └── yiran-ding-IrGyuTSrkK4-unsplash.jpg         # Night street (dark)
 └── results/                      # TÜM çıktıların kaydedildiği klasör (otomatik oluşur)
```

**Gereksinimler:**

```bash
pip install numpy opencv-python matplotlib
```

**Çalıştırma:**

```bash
cd odev3
python main.py
```

---

## 3) Kodun Çalışma Mantığı (Adım Adım)

Aşağıdaki adımlar **main.py** içinde otomatik olarak yürütülür ve her görüntü için aynı sıra uygulanır:

1. **Görüntü Okuma + Gri-Seviye Dönüşümü**  
   - `cv2.imread(..., cv2.IMREAD_GRAYSCALE)` ile okunur.  
   - Tüm resimler aynı boyuta getirilir: **256×256** (adil karşılaştırma için).
   - `results/` içine `*_gray.jpg` olarak kaydedilir.

2. **Soru 1 – Temel Nokta İşlemleri (`point_operations.py`)**
   - **Parlaklık Ayarı:** `adjust_brightness(img, ±40)` → `*_bright_plus.jpg`, `*_bright_minus.jpg`
   - **Kontrast Ayarı:** `adjust_contrast(img, 1.5)` ve `adjust_contrast(img, 0.7)` → `*_contrast_1_5.jpg`, `*_contrast_0_7.jpg`
     - Formül: `out = factor * (in - 128) + 128`
   - **Negatif Görüntü:** `image_negative(img)` → `*_negative.jpg`
     - Formül: `out = 255 - in`
   - **Eşikleme:** `threshold(img, T)` → `*_thresh_T.jpg` (T = medyan)
     - Kural: `in > T → 255, aksi 0`

3. **Soru 2 – Histogram & İstatistikler (`histogram_processing.py`)**
   - **Histogram (manuel):** `compute_histogram(img)` → 256 binli sayım
   - **Görselleştirme:** `results/{stem}_orig_hist.png`
   - **İstatistikler:** `image_stats(img)` → `results/{stem}_stats.txt`
     - **mean** (ortalama), **std** (standart sapma), **entropy** (−Σ p log₂ p), **min**, **max**

4. **Soru 3 – Kontrast Germe**
   - `contrast_stretch(img)` → `*_stretched.jpg`
   - **2×2 Karşılaştırma Görseli:** `*_stretch_2x2.png`  
     - Üst satır: orijinal & gerilmiş görüntü  
     - Alt satır: her ikisinin histogramı  
   - Formül: `out = (in − min) / (max − min) * 255`

5. **Soru 4 – Histogram Eşitleme (manuel)**
   - `hist_equalize(img)` → `*_histeq.jpg`
   - **2×2 Karşılaştırma Görseli:** `*_histeq_2x2.png`  
     - Adımlar: `hist → pdf → cdf → LUT = floor(255*cdf) → map`

6. **Soru 5 – Gamma Düzeltmesi**
   - `gamma_correction(img, γ)` → `*_gamma_0_5.jpg`, `*_gamma_1_0.jpg`, `*_gamma_1_5.jpg`, `*_gamma_2_0.jpg`, `*_gamma_2_5.jpg`
   - Formül: `out = 255 * (in/255)^γ`  
     - **γ < 1:** karanlık bölgeleri aydınlatır  
     - **γ > 1:** parlaklığı bastırır, parlak alanları koyulaştırır

---

## 4) Sonuçların Konumu ve İsimlendirme

Tüm çıktılar **otomatik olarak** `results/` klasörüne kaydedilir. Dosya adları **girdi dosya adının gövdesi** (stem) + **işlem etiketi** formatındadır. Örnekler:

- `inggrid-koe-kbKEuU-YEIw-unsplash_gray.jpg` – gri-seviye
- `..._bright_plus.jpg`, `..._bright_minus.jpg` – parlaklık ±40
- `..._contrast_1_5.jpg`, `..._contrast_0_7.jpg` – kontrast
- `..._negative.jpg` – negatif
- `..._thresh_XXX.jpg` – eşikleme (XXX = kullanılan T değeri)
- `..._orig_hist.png` – orijinal histogramı
- `..._stats.txt` – istatistik değerleri (mean, std, entropy, min, max)
- `..._stretched.jpg` ve `..._stretch_2x2.png` – kontrast germe sonucu ve 2×2 sunumu
- `..._histeq.jpg` ve `..._histeq_2x2.png` – histogram eşitleme sonucu ve 2×2 sunumu
- `..._gamma_0_5.jpg ... _gamma_2_5.jpg` – gamma deneyleri

Bu isimlendirme, rapora görselleri eklerken **hangi işlemin** sonucu olduğunu hızlıca anlamayı sağlar.

---

## 5) Dosya Bazlı Açıklamalar

### `point_operations.py`
- `adjust_brightness`: Sabit ekleyip kırpma (0–255) yapılır.
- `adjust_contrast`: 128 etrafında doğrusal ölçekleme.
- `image_negative`: Tüm tonları tersine çevirir.
- `threshold`: İkili görüntü; segmentasyon örnekleri için temel adımdır.
- `gamma_correction`: İnsan görsel algısına uygun **nonlineer** ton eşitleme.

### `histogram_processing.py`
- `compute_histogram`: For döngüsü ile **manuel** histogram; 256 bin.
- `image_stats`: `mean`, `std`, **entropy** (p>0 için −Σ p log₂ p), `min`, `max`.
- `contrast_stretch`: Dinamik aralığı 0–255’e yayar; düşük kontrastlı görsellerde faydalıdır.
- `hist_equalize`: **CDF** tabanlı dönüştürme; global kontrastı dengeler, koyu/aydınlık bölgelerin dağılımını homojenleştirir.

### `main.py`
- Test görselleri listesi **özel olarak** şu dört dosyaya sabitlenmiştir:  
  `inggrid-koe-kbKEuU-YEIw-unsplash.jpg`, `michael-tomlinson-ih2JHLPy6vg-unsplash.jpg`, `vladut-anton-Q0GHqEaHEhA-unsplash.jpg`, `yiran-ding-IrGyuTSrkK4-unsplash.jpg`  
- Her biri sırayla Soru 1–5 fonksiyonlarına gönderilir ve sonuçlar kaydedilir.

---

## 6) Hangi Görsel Hangi Test İçin? (Öneri)

- **Foggy forest** → Düşük kontrast → *Kontrast germe* & *Histogram eşitleme*
- **Bridge B&W** → Yüksek kontrast → *Eşikleme* & *Negatif*
- **Bright field** → Aşırı parlak → *Gamma (γ > 1)* & *Parlaklık azaltma*
- **Night street** → Karanlık → *Gamma (γ < 1)* & *Parlaklık artırma*

---

## 7) Sık Karşılaşılan Sorunlar

- **Resim okunamıyor:** `test_images/` içindeki dosya isimleri **tam olarak** koddaki isimlerle aynı olmalı ve `.jpg` uzantısı görünür olmalıdır.
- **Grafik pencereleri açılmıyor:** Kod görselleri **dosyaya kaydeder**, ekranda göstermez. `results/` klasörünü kontrol edin.
- **Tüm pikseller aynı ise (min=max):** `contrast_stretch` fonksiyonu sıfır görüntü döndürür; bu durum normaldir.

---

## 8) Rapor İçin Kısa Yol

Raporunuzda aşağıdaki görselleri kullanmanız önerilir:
- `*_stretch_2x2.png` ve `*_histeq_2x2.png` → Hem **görüntü** hem **histogram** birlikte
- `*_stats.txt` → İstatistik tabloları
- `*_gamma_*.jpg` → Farklı gamma değerlerinin etkisi (0.5, 1.0, 1.5, 2.0, 2.5)

**Not:** Açıklama yaparken formülleri (README’de verilen) ve gözlemlerinizi ekleyin.

---

## 9) Katkı ve Lisans

- Kodlar eğitim amaçlıdır. Görseller Unsplash lisansı kapsamındadır (fotoğrafçı sayfalarından bakınız).

---

Başarılar!  

**Omar A.M. Issa – 220212901**
