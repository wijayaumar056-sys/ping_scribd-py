import xmlrpc.client
import os

# Mempertahankan variabel asli yang terbukti sukses di GitHub Actions Anda
BLOG_NAME = "GuruPertama.com"
URL_FILE = "urls.txt"
JUMLAH_PROSES = 5  # Memproses 5 URL sekaligus sekali jalan

# Hanya menyisakan server yang statusnya "Success" berdasarkan file image_d2c5a1.png
RPC_SERVERS = [
    "http://rpc.pingomatic.com/",
    "http://rpc.twingly.com/",
    "http://ping.blo.gs/"
]

def send_rpc_ping(server, title, url):
    try:
        # Ditambahkan timeout 10 detik agar tidak macet jika salah satu server lambat
        rpc_server = xmlrpc.client.ServerProxy(server, timeout=10)
        result = rpc_server.weblogUpdates.ping(title, url)
        print(f"  ✅ Success: {server}")
    except:
        print(f"  ❌ Failed: {server}")

def main():
    if not os.path.exists(URL_FILE):
        print(f"File {URL_FILE} tidak ada!")
        return
        
    # 1. Baca semua baris dari file urls.txt
    with open(URL_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]
        
    # Saring baris yang berisi URL aktif (bukan komentar atau baris kosong)
    urls = [line for line in lines if line and not line.startswith('#')]

    if not urls:
        print("💡 Tidak ada URL aktif di dalam daftar untuk diproses.")
        return

    # Tentukan jumlah URL yang akan dieksekusi (maksimal 5 atau sisa URL yang ada)
    total_di_proses = min(JUMLAH_PROSES, len(urls))
    print(f"🚀 Menjalankan Ping Otomatis untuk {total_di_proses} URL Sekaligus...\n")

    # Ambil 5 URL teratas dari antrean
    urls_to_process = urls[:total_di_proses]

    # 2. Lakukan perulangan ping untuk 5 URL tersebut
    for index, target_url in enumerate(urls_to_process, 1):
        print(f"[{index}/{total_di_proses}] 🧐 Ping: {target_url}")
        for server in RPC_SERVERS:
            send_rpc_ping(server, BLOG_NAME, target_url)
            
        # 3. Pindahkan URL yang sudah diproses dari atas ke baris paling bawah di memori
        if target_url in lines:
            lines.remove(target_url)  # Hapus dari baris atas
            lines.append(target_url)   # Tempel ke baris paling bawah
        print(f"  🔄 URL digeser ke daftar paling bawah.\n")

    # 4. Tulis ulang semua perubahan urutan antrean ke dalam file urls.txt
    with open(URL_FILE, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
            
    print(f"🏁 Selesai! Antrean file {URL_FILE} telah diperbarui secara otomatis.")

if __name__ == "__main__":
    main()
