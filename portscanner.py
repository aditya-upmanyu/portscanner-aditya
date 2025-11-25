import socket
import threading
from queue import Queue
from termcolor import colored
import sys

# --- CONFIGURATION ---
# How many threads to use (simultaneous checks)
# 50-100 is safe for home networks. Too high might crash your router.
THREAD_COUNT = 50 
TIMEOUT = 0.5

# Initialize queue for threading
queue = Queue()
print_lock = threading.Lock() # Prevents text from overlapping

def grab_banner(s):
    """
    Attempts to read the first few bytes from the service to identify it.
    """
    try:
        # Send a simple query to trigger a response (works for some services)
        # Many services will send a banner automatically on connect.
        return s.recv(1024).decode().strip()
    except:
        return "Unknown Service"

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((target, port))
        
        # If connection successful, try to grab the banner
        try:
            banner = grab_banner(sock)
        except:
            banner = "N/A"
            
        with print_lock:
            print(colored(f"[+] Port {port} Open | Service: {banner}", 'green'))
            
        sock.close()
    except:
        # Port is closed or filtered
        pass

def threader(target):
    """
    Worker thread: pulls a port from the queue and scans it.
    """
    while True:
        port_to_scan = queue.get()
        scan_port(target, port_to_scan)
        queue.task_done()

def run_scanner(target, ports):
    print(colored(f"\n[*] Starting Fast Scan for: {target}", 'blue'))
    print(colored(f"[*] Threads: {THREAD_COUNT}", 'yellow'))

    # 1. Create worker threads
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=threader, args=(target,))
        t.daemon = True # Kill thread when main program exits
        t.start()

    # 2. Fill the queue with ports
    for port in range(1, ports + 1):
        queue.put(port)

    # 3. Wait for queue to be empty
    queue.join()
    print(colored("[*] Scan Complete\n", 'blue'))

if __name__ == "__main__":
    # Initialize colorama for Windows
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass

    try:
        targets_input = input("[*] Enter Target IP(s) (split by ,): ")
        ports_input = int(input("[*] Enter Max Port to Scan (e.g. 1000): "))
        
        targets = [t.strip() for t in targets_input.split(',')]

        for target in targets:
            run_scanner(target, ports_input)
            
    except KeyboardInterrupt:
        print(colored("\n[!] Exiting...", 'red'))
        sys.exit()
    except ValueError:
        print(colored("[!] Invalid input.", 'red'))
