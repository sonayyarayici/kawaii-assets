import os

# --- AYARLAR ---
# Burası senin assetlerinin olduğu ana klasör
ROOT_DIR = "D:\Appventure\Kawaii Wallpapers\contents\drive-download-20240804T152221Z-001" # Scriptin çalıştığı klasörü otomatik alır

def clean_files():
    print("🗑️ Temizlik Başlıyor: .gif ve .mp4 dosyaları aranıyor...")
    deleted_count = 0
    
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        for file in filenames:
            # Sadece gif ve mp4'leri hedef al
            if file.lower().endswith(('.gif', '.mp4')):
                file_path = os.path.join(dirpath, file)
                
                try:
                    os.remove(file_path)
                    print(f"❌ Silindi: {file}")
                    deleted_count += 1
                except Exception as e:
                    print(f"⚠️ Silinemedi: {file} - Hata: {e}")

    print(f"\n✨ İşlem Tamam! Toplam {deleted_count} dosya silindi.")
    print("❗ UNUTMA: Şimdi 'git add' ve 'git push' yaparak GitHub'ı güncellemelisin.")

if __name__ == "__main__":
    clean_files()