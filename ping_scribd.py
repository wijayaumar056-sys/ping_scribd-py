import xmlrpc.client
import os
from urllib.parse import urlparse

URL_FILE = "urls.txt"

# Menyisakan server ping utama yang aktif dan mendukung multiplatform
RPC_SERVERS = [
    "http://rpc.pingomatic.com/",
    "http://rpc.twingly.com/"
]

def get_dynamic_blog_name(url):
    """
    Otomatis mendeteksi nama platform/domain dari URL agar RPC server 
    menerima nama pengirim yang relevan (misal: 'docs.google.com' atau 'scribd.com')
    """
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        # Menghilangkan 'www.' jika ada agar lebih rapi
        if domain.startswith("www."):
            domain = domain[4:]
        return domain if domain else "Educational Resource"
    except:
        return "Educational Resource"

def send_rpc_ping(server, title, url):
    try:
        # Menggunakan timeout 10 detik agar eksekusi tidak macet jika server lambat
        rpc_server = xmlrpc.client.ServerProxy(server, timeout=10)
        result = rpc_server.weblogUpdates.ping(title, url)
        print(f"  ✅ Success Ping [{title}] -> {server}")
    except Exception as e:
        print(f"  ❌ Failed Ping [{title}] -> {server}")

def main():
    if not os.path.exists(URL_FILE):
        print(f"❌ File {URL_FILE} tidak ditemukan!")
        return

    # 1. Baca semua baris dari file urls.txt
    with open(URL_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]
    
    # Saring hanya baris yang berisi URL aktif (bukan komentar atau baris kosong)
    urls = [line for line in lines if line and not line.startswith('#')]

    if not urls:
        print("💡 Tidak ada URL aktif di dalam daftar untuk diproses.")
        return

    # 2. Ambil URL pertama (paling atas) dalam antrean
    target_url = urls[0]
    
    # Deteksi otomatis nama pengirim berdasarkan domain target (Google Docs, Scribd, dll.)
    dynamic_name = get_dynamic_blog_name(target_url)
    
    print(f"🧐 Memproses Antrean Teratas:")
    print(f"🔗 URL : {target_url}")
    print(f"🏷️ Tag : {dynamic_name}\n")
    
    # Kirim ping rpc
    for server in RPC_SERVERS:
        send_rpc_ping(server, dynamic_name, target_url)

    # 3. Otomatisasi Pemindahan: Geser URL yang sudah diproses ke paling bawah
    lines.remove(target_url)
    lines.append(target_url)

    # 4. Tulis kembali perubahan ke file urls.txt
    with open(URL_FILE, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
            
    print(f"\n🔄 Otomatisasi Sukses: URL di atas berhasil digeser ke daftar paling bawah file {URL_FILE}.")

if __name__ == "__main__":
    main()
