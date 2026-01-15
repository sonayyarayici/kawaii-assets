import os
import re

def dogal_siralama_anahtari(metin):
    """
    Dosyaları 1, 2, 10, 20 şeklinde (insan mantığıyla) sıralamak için yardımcı fonksiyon.
    Aksi takdirde bilgisayar 1, 10, 2 şeklinde sıralar.
    """
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', metin)]

def klasorleri_duzenle(ana_klasor_yolu):
    # Ana klasör ve tüm alt klasörleri gez
    for kok_dizin, klasorler, dosyalar in os.walk(ana_klasor_yolu):
        
        # Sadece .webp uzantılı dosyaları bul
        webp_dosyalari = [f for f in dosyalar if f.lower().endswith('.webp')]
        
        # Eğer klasörde webp yoksa pas geç
        if not webp_dosyalari:
            continue
            
        print(f"İşleniyor: {kok_dizin} ({len(webp_dosyalari)} dosya)")

        # Dosyaları mevcut isimlerindeki sayılara göre sırala (1, 5, 10, 12...)
        # Bu sayede mevcut sırayı bozmadan boşlukları kapatmış oluruz.
        webp_dosyalari.sort(key=dogal_siralama_anahtari)

        # ADIM 1: Önce hepsine geçici bir isim ver (Çakışmayı önlemek için)
        # temp_random_1.webp, temp_random_2.webp gibi...
        gecici_isimler = []
        for index, eski_isim in enumerate(webp_dosyalari, start=1):
            eski_yol = os.path.join(kok_dizin, eski_isim)
            
            # Geçici isim oluştur
            yeni_gecici_isim = f"temp_rename_{index}.webp"
            yeni_gecici_yol = os.path.join(kok_dizin, yeni_gecici_isim)
            
            os.rename(eski_yol, yeni_gecici_yol)
            gecici_isimler.append(yeni_gecici_isim)

        # ADIM 2: Geçici isimleri nihai isimlere (1.webp, 2.webp) çevir
        for index, gecici_isim in enumerate(gecici_isimler, start=1):
            gecici_yol = os.path.join(kok_dizin, gecici_isim)
            
            # Nihai isim (1.webp, 2.webp...)
            nihai_isim = f"{index}.webp"
            nihai_yol = os.path.join(kok_dizin, nihai_isim)
            
            os.rename(gecici_yol, nihai_yol)

    print("\n✅ Tüm işlemler başarıyla tamamlandı!")

# --- KULLANIM ---
# Aşağıdaki tırnak içine ana klasörünün yolunu yapıştır.
# Örnek Windows yolu: r"C:\Users\Adın\Desktop\Resimlerim"
# Örnek Mac/Linux yolu: "/Users/Adin/Desktop/Resimlerim"

hedef_klasor = r"D:\Appventure\Kawaii Wallpapers\contents\drive-download-20240804T152221Z-001"

# Kodu çalıştır
if os.path.exists(hedef_klasor):
    klasorleri_duzenle(hedef_klasor)
else:
    print("HATA: Belirtilen klasör yolu bulunamadı.")