import xmlrpc.client
import os

BLOG_NAME = "GuruPertama.com"
URL_FILE = "urls.txt"

# Menyisakan server ping yang valid dan responsif
RPC_SERVERS = [
    "http://rpc.pingomatic.com/",
    "http://rpc.twingly.com/"
]

def send_rpc_ping(server, title, url):
    try:
        # Menambahkan timeout agar script tidak macet jika server lambat merespons
        rpc_server = xmlrpc.client.ServerProxy(server, timeout=10)
        result = rpc_server.weblogUpdates.ping(title, url)
        print(f"  ✅ Success: {server}")
    except Exception as e:
        print(f"  ❌ Failed: {server}")

def main():
    if not os.path.exists(URL_FILE):
        print(f"❌ File {URL_FILE} tidak ditemukan!")
        return

    # 1. Baca semua baris dari file urls.txt
    with open(URL_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]
    
    # Saring baris yang berisi URL aktif (bukan komentar atau baris kosong)
    urls = [line for line in lines if line and not line.startswith('#')]

    if not urls:
        print("💡 Tidak ada URL aktif di dalam daftar untuk diproses.")
        return

    # 2. Ambil URL pertama (paling atas) untuk diproses ping
    target_url = urls[0]
    print(f"🧐 Memproses Ping untuk URL teratas: {target_url}")
    
    for server in RPC_SERVERS:
        send_rpc_ping(server, BLOG_NAME, target_url)

    # 3. Otomatisasi Pemindahan: Geser URL yang sudah diproses ke paling bawah
    # Hapus URL ini dari posisi pertamanya
    lines.remove(target_url)
    # Tambahkan kembali URL ini ke baris paling akhir dokumen
    lines.append(target_url)

    # 4. Tulis ulang file urls.txt dengan urutan yang baru
    with open(URL_FILE, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
            
    print(f"🔄 Otomatisasi Sukses: {target_url} telah dipindahkan ke daftar paling bawah.\n")

if __name__ == "__main__":
    main()
