# Prokudin-Gorskii Renkli Görüntü Yeniden Yapılandırma

**Öğrenci:** Omar A.M. Issa
**Numara:** 220212901
**Üniversite:** OSTİM Teknik Üniversitesi

## Proje Açıklaması
Bu proje, tarihî **Prokudin-Gorskii** fotoğraflarını yeniden renklendirmek amacıyla geliştirilmiştir.
Program aşağıdaki adımları gerçekleştirir:
- Üst üste yığılmış gri tonlamalı görüntüleri **Mavi, Yeşil ve Kırmızı (B, G, R)** kanallarına ayırır.
- Kanalları **NCC (Normalized Cross-Correlation)** veya **SSD (Sum of Squared Differences)** yöntemleriyle hizalar.
- İsteğe bağlı olarak **çok ölçekli piramit hizalama** (pyramid alignment) uygular.
- Son görüntüyü **histogram eşitleme**, **gamma düzeltmesi** ve **keskinleştirme (unsharp masking)** yöntemleriyle iyileştirir.
- Görüntü kenarlarındaki siyah çerçeveleri **otomatik olarak kırpar**.

## Kullanım
Terminalden aşağıdaki komutu çalıştırın:
```bash
python main.py --input ../data --output ../results --metric ncc --pyramid
