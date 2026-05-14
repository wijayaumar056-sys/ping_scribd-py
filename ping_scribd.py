import requests
import xmlrpc.client
import os

BLOG_NAME = "GuruPertama.com"
URL_FILE = "urls.txt"

RPC_SERVERS = [
    "http://rpc.pingomatic.com/",
    "http://rpc.twingly.com/",
    "http://api.feedburner.com/ping",
    "http://www.blogdigger.com/RPC2",
    "http://rpc.weblogs.com/RPC2",
    "http://ping.blo.gs/"
]

def send_rpc_ping(server, title, url):
    try:
        rpc_server = xmlrpc.client.ServerProxy(server)
        result = rpc_server.weblogUpdates.ping(title, url)
        print(f"✅ Success: {server}")
    except:
        print(f"❌ Failed: {server}")

def main():
    if not os.path.exists(URL_FILE):
        print("File urls.txt tidak ada!")
        return
    with open(URL_FILE, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    for target_url in urls:
        print(f"🧐 Ping: {target_url}")
        for server in RPC_SERVERS:
            send_rpc_ping(server, BLOG_NAME, target_url)

if __name__ == "__main__":
    main()
