import os
import json

# --- AYARLAR (Buraları Kendi Bilgilerinle Değiştir) ---
ROOT_DIR = r"D:\Appventure\Kawaii Wallpapers\contents\drive-download-20240804T152221Z-001"  # Klasörlerinin olduğu yer
GITHUB_BASE_URL = "https://raw.githubusercontent.com/sonayyarayici/kawaii-assets/main"

# --- FİYATLANDIRMA KURALLARI ---
COST_IMAGE = 300  # .webp, .jpg, .png
COST_GIF = 600    # .gif
COST_VIDEO = 1000 # .mp4

def generate_data_json():
    data = {
        "version": 1,
        "categories": []
    }

    # Klasörleri alfabetik sıraya göre gez
    folder_names = sorted([d for d in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, d)) and not d.startswith('.')])

    for folder in folder_names:
        folder_path = os.path.join(ROOT_DIR, folder)
        files = sorted(os.listdir(folder_path))
        
        category_items = []
        cover_image = ""

        for file in files:
            # Sadece medya dosyalarını al (Sistem dosyalarını vs görmezden gel)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4')):
                
                # Dosya uzantısını ve adını ayır
                file_name_only = os.path.splitext(file)[0]
                extension = os.path.splitext(file)[1].lower()
                
                # URL oluştur
                file_url = f"{GITHUB_BASE_URL}/{folder}/{file}"
                
                # Temel Öğe Yapısı
                item = {
                    "id": f"{folder}_{file_name_only}", # Örn: Anime_1
                    "url": file_url,
                    "premium": False # Varsayılan hepsi ücretsiz (kredi ile açılır)
                }

                # --- MANTIKSAL AYRIŞTIRMA VE FİYATLANDIRMA ---
                
                # 1. VİDEO (Live Wallpaper)
                if extension == '.mp4':
                    item['type'] = 'video'
                    item['cost'] = COST_VIDEO
                    
                    # Thumbnail Bulma Mantığı:
                    # Video adı "car.mp4" ise, klasörde "car.webp" veya "car.jpg" var mı diye bakar.
                    # Yoksa, kategorinin kapak resmini kullanır.
                    thumb_candidate = f"{file_name_only}.webp"
                    if thumb_candidate in files:
                        item['thumbnail'] = f"{GITHUB_BASE_URL}/{folder}/{thumb_candidate}"
                    else:
                        # Eğer özel thumbnail yoksa, kategorinin ilk resmini verelim
                        item['thumbnail'] = f"{GITHUB_BASE_URL}/{folder}/1.webp" 

                # 2. GIF (Hareketli Resim)
                elif extension == '.gif':
                    item['type'] = 'gif'
                    item['cost'] = COST_GIF
                    item['thumbnail'] = file_url # GIF'in kapağı kendisidir

                # 3. STATİK RESİM (WebP, JPG, PNG)
                else:
                    item['type'] = 'image'
                    item['cost'] = COST_IMAGE
                    item['thumbnail'] = file_url
                    
                    # Eğer henüz kapak resmi seçilmediyse, ilk bulunan resmi kapak yap
                    if cover_image == "":
                        cover_image = file_url

                # Thumbnail dosyalarını (örn: video_thumb.webp) ana listeye ekleme
                # Sadece ana içerikleri ekle. 
                # Eğer bir dosya .mp4 ise ekle, ama o mp4'ün .webp versiyonunu listede gösterme (o sadece kapaktır)
                is_thumbnail_for_video = False
                if extension != '.mp4':
                    # Eğer bu isimde bir .mp4 varsa, bu dosya muhtemelen onun kapağıdır
                    if f"{file_name_only}.mp4" in files:
                        is_thumbnail_for_video = True
                
                if not is_thumbnail_for_video:
                    category_items.append(item)

        # Kategoriyi listeye ekle (Eğer içi boş değilse)
        if category_items:
            data["categories"].append({
                "id": folder,
                "name": folder.replace("-", " "), # URL dostu ismi Okunabilir yap (Cute-Minimal -> Cute Minimal)
                "cover": cover_image if cover_image else "",
                "items": category_items
            })
            print(f"✅ Kategori: {folder} | İçerik: {len(category_items)} adet")

    # JSON dosyasını kaydet
    output_path = os.path.join(ROOT_DIR, "data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 data.json oluşturuldu! Konum: {output_path}")
    print(f"💰 Fiyatlar: Resim={COST_IMAGE}, Gif={COST_GIF}, Video={COST_VIDEO}")

if __name__ == "__main__":
    generate_data_json()