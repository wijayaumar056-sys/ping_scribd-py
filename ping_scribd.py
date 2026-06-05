import xmlrpc.client
import os
from urllib.parse import urlparse

URL_FILE = "urls.txt"
JUMLAH_PROSES = 5  # Memproses 5 URL sekaligus sekali jalan

RPC_SERVERS = [
    "http://rpc.pingomatic.com/",
    "http://rpc.twingly.com/"
]

def get_dynamic_blog_name(url):
    """
    Membuat nama judul yang valid dan disukai server RPC agar tidak di-banned.
    """
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        
        # Ditambahkan kata kunci edukatif di depannya agar lolos filter spam server RPC
        if "docs.google" in domain:
            return "Google Docs Educational Resource"
        elif "scribd" in domain:
            return "Scribd Share Document"
        elif "slideshare" in domain:
            return "SlideShare Presentation"
        elif "academia" in domain:
            return "Academia Edu Research Paper"
        else:
            return f"Guru Pertama Resource - {domain}"
    except:
        return "Guru Pertama Educational Resource"

def send_rpc_ping(server, title, url):
    try:
        # Diturunkan timeout ke 5 detik agar jika salah satu server down, script tidak macet lama
        rpc_server = xmlrpc.client.ServerProxy(server, timeout=5)
        result = rpc_server.weblogUpdates.ping(title, url)
        print(f"    ✅ Success: {server}")
        return True
    except Exception as e:
        print(f"    ❌ Failed: {server}")
        return False

def main():
    if not os.path.exists(URL_FILE):
        print(f"❌ File {URL_FILE} tidak ditemukan!")
        return

    # 1. Baca semua baris dari file
    with open(URL_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]
    
    # Saring baris yang berisi URL aktif (bukan komentar atau baris kosong)
    urls = [line for line in lines if line and not line.startswith('#')]

    if not urls:
        print("💡 Tidak ada URL aktif di dalam daftar urls.txt untuk diproses.")
        return

    # Tentukan berapa banyak yang akan diproses (maksimal sejumlah URL yang tersedia)
    total_di_proses = min(JUMLAH_PROSES, len(urls))
    print(f"🚀 Menjalankan Ping Otomatis untuk {total_di_proses} URL Sekaligus...\n")

    # Ambil daftar URL yang akan diproses kali ini (5 URL teratas)
    urls_to_process = urls[:total_di_proses]

    for index, target_url in enumerate(urls_to_process, 1):
        dynamic_title = get_dynamic_blog_name(target_url)
        
        print(f"[{index}/{total_di_proses}] 🧐 Memproses Ping:")
        print(f"  🔗 URL : {target_url}")
        print(f"  🏷️ Tag : {dynamic_title}")
        
        # Jalankan ping ke semua server RPC
        for server in RPC_SERVERS:
            send_rpc_ping(server, dynamic_title, target_url)
        
        # 3. Proses pemindahan posisi di dalam memori list 'lines'
        if target_url in lines:
            lines.remove(target_url)  # Hapus dari atas
            lines.append(target_url)  # Tempel ke paling bawah
        print(f"  🔄 URL digeser ke baris paling bawah.\n")

    # 4. Tulis ulang semua urutan baru ke file urls.txt setelah loop selesai
    with open(URL_FILE, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
            
    print(f"🏁 Selesai! File {URL_FILE} berhasil diperbarui dengan urutan antrean yang baru.")

if __name__ == "__main__":
    main()
