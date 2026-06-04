#!/usr/bin/env python3
"""
DarkBuster - Advanced Web Directory & File Bruteforcer
Author: Manjeet Thakur (darkdisaster08)
GitHub: https://github.com/darkdisaster08
Wordlists updated: May 2026
VERSION = "1.1.1"
darkbuster --version
"""

import argparse
import sys
import os
import threading
import time
import signal
from queue import Queue
from datetime import datetime

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("[!] Missing dependency: requests")
    print("[*] Run: pip3 install requests")
    sys.exit(1)

# ─────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────
class Color:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"

def red(t):    return f"{Color.RED}{t}{Color.RESET}"
def green(t):  return f"{Color.GREEN}{t}{Color.RESET}"
def yellow(t): return f"{Color.YELLOW}{t}{Color.RESET}"
def blue(t):   return f"{Color.BLUE}{t}{Color.RESET}"
def cyan(t):   return f"{Color.CYAN}{t}{Color.RESET}"
def bold(t):   return f"{Color.BOLD}{t}{Color.RESET}"

# ─────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────
BANNER = f"""
{Color.CYAN}{Color.BOLD}
██████╗  █████╗ ██████╗ ██╗  ██╗██████╗ ██╗   ██╗███████╗████████╗███████╗██████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██║  ██║███████║██████╔╝█████╔╝ ██████╔╝██║   ██║███████╗   ██║   █████╗  ██████╔╝
██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██████╔╝██║  ██║██║  ██║██║  ██╗██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{Color.RESET}
{Color.GREEN}  Advanced Web Directory & File Bruteforcer{Color.RESET}
{Color.YELLOW}  By: Manjeet Thakur (darkdisaster08){Color.RESET}
{Color.BLUE}  GitHub: https://github.com/darkdisaster08{Color.RESET}
{Color.CYAN}  Wordlists Updated: May 2026{Color.RESET}
{Color.RED}  For authorized security testing only!{Color.RESET}
"""

# ─────────────────────────────────────────
#  GLOBALS
# ─────────────────────────────────────────
found_paths   = []
scanned_count = 0
lock          = threading.Lock()
stop_event    = threading.Event()

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def get_wordlist_path(name):
    base = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "wordlists"
    )

    if os.path.isabs(name):
        return name

    if name.startswith("wordlists/"):
        name = name[len("wordlists/"):]

    return os.path.join(base, name)

def load_wordlist(path):
    if not os.path.exists(path):
        print(red(f"[!] Wordlist not found: {path}"))

        wl_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "wordlists"
        )

        print(yellow("\nAvailable wordlists:\n"))

        if os.path.isdir(wl_dir):
            for root, _, files in os.walk(wl_dir):
                for file in files:
                    if file.endswith(".txt"):
                        rel = os.path.relpath(
                            os.path.join(root, file),
                            wl_dir
                        )
                        print(f"  - {rel}")

        sys.exit(1)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

def normalize_url(url):
    return url.rstrip("/")

def status_color(code):
    if code in [200, 201]:      return green(str(code))
    elif code in [301, 302, 307, 308]: return yellow(str(code))
    elif code == 403:           return red(str(code))
    elif code == 401:           return cyan(str(code))
    else:                       return str(code)

def signal_handler(sig, frame):
    print(yellow("\n[!] Scan interrupted by user. Saving results..."))
    stop_event.set()

signal.signal(signal.SIGINT, signal_handler)

# ─────────────────────────────────────────
#  SCANNER
# ─────────────────────────────────────────
def scanner(queue, base_url, extensions, timeout, status_codes, output_file, session):
    global scanned_count

    while not queue.empty() and not stop_event.is_set():
        word = queue.get()

        targets = [f"{base_url}/{word}"]

        for ext in extensions:
            targets.append(f"{base_url}/{word}{ext}")

        for target in targets:
            if stop_event.is_set():
                break

            try:
                resp = session.get(
                    target,
                    timeout=timeout,
                    allow_redirects=False,
                    verify=False
                )

                with lock:
                    scanned_count += 1

                    if resp.status_code in status_codes:
                        size = len(resp.content)

                        msg = (
                            f"[{status_color(resp.status_code)}] "
                            f"{target} (Size: {size})"
                        )

                        print(msg)

                        found_paths.append(
                            f"[{resp.status_code}] {target} (Size: {size})"
                        )

                        if output_file:
                            with open(output_file, "a") as f:
                                f.write(
                                    f"[{resp.status_code}] "
                                    f"{target} (Size: {size})\n"
                                )

            except requests.exceptions.ConnectionError:
                with lock:
                    scanned_count += 1

            except requests.exceptions.Timeout:
                with lock:
                    scanned_count += 1

            except Exception:
                with lock:
                    scanned_count += 1

            queue.task_done()

# ─────────────────────────────────────────
#  PROGRESS DISPLAY
# ─────────────────────────────────────────
def show_progress(total, start_time):
        with lock:
            count = scanned_count
        elapsed = time.time() - start_time
        speed = int(count / elapsed) if elapsed > 0 else 0
        remaining = total - count
        eta = int(remaining / speed) if speed > 0 else 0
        print(f"\r{cyan(f'Progress: {count}/{total} | Speed: {speed} req/s | ETA: {eta}s')}   ", end="", flush=True)
        if count >= total:
            break
        time.sleep(0.5)

# ─────────────────────────────────────────
#  AVAILABLE WORDLISTS
# ─────────────────────────────────────────
def list_wordlists():
    base = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "wordlists"
    )

    print(bold("\n[*] Available Wordlists:\n"))

    if not os.path.isdir(base):
        print(red("[!] wordlists directory not found"))
        return

    for root, _, files in os.walk(base):
        for file in sorted(files):
            if file.endswith(".txt"):
                rel = os.path.relpath(
                    os.path.join(root, file),
                    base
                )

                fpath = os.path.join(root, file)

                try:
                    count = sum(
                        1 for _
                        in open(
                            fpath,
                            encoding="utf-8",
                            errors="ignore"
                        )
                    )
                except:
                    count = 0

                print(
                    f"{green(rel)} "
                    f"{yellow(f'({count} entries)')}"
                )

    print()

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="DarkBuster — Advanced Web Directory & File Bruteforcer",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-u", "--url",         help="Target URL (e.g. http://example.com)", required=False)
    parser.add_argument("-w", "--wordlist",    help="Wordlist to use (default: common)", default="common.txt")
    parser.add_argument("-t", "--threads",     help="Number of threads (default: 20)", type=int, default=20)
    parser.add_argument("-x", "--extensions",  help="Extensions to append (e.g. .php,.html,.bak)", default="")
    parser.add_argument("-o", "--output",      help="Save results to file")
    parser.add_argument("-s", "--status",      help="Status codes to show (default: 200,301,302,403,401)", default="200,301,302,307,401,403")
    parser.add_argument("--timeout",           help="Request timeout in seconds (default: 5)", type=int, default=5)
    parser.add_argument("--user-agent",        help="Custom User-Agent string")
    parser.add_argument("--cookie",            help="Cookie header (e.g. 'session=abc123')")
    parser.add_argument("--list-wordlists",    help="Show all available wordlists", action="store_true")
    parser.add_argument("--no-color",          help="Disable colored output", action="store_true")

    args = parser.parse_args()

    if args.list_wordlists:
        list_wordlists()
        sys.exit(0)

    if not args.url:
        parser.print_help()
        print(red("\n[!] Error: Target URL is required. Use -u <url>"))
        sys.exit(1)

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        print(red("[!] URL must start with http:// or https://"))
        sys.exit(1)

    base_url = normalize_url(args.url)

    # Resolve wordlist path
    wl_path = args.wordlist
    if not os.path.isabs(wl_path):
        wl_path = get_wordlist_path(args.wordlist)

    words = load_wordlist(wl_path)

    extensions = [e if e.startswith(".") else f".{e}"
                  for e in args.extensions.split(",") if e.strip()] if args.extensions else []

    status_codes = [int(s.strip()) for s in args.status.split(",")]

    # Setup session
    session = requests.Session()
    ua = args.user_agent or "DarkBuster/1.0 (github.com/darkdisaster08)"
    headers = {"User-Agent": ua}
    if args.cookie:
        headers["Cookie"] = args.cookie
    session.headers.update(headers)

    # Output file setup
    if args.output:
        with open(args.output, "w") as f:
            f.write(f"DarkBuster Scan Results\n")
            f.write(f"Target: {base_url}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Wordlist: {wl_path}\n")
            f.write("=" * 60 + "\n\n")

    # Scan info
    total_words = len(words) * (1 + len(extensions))
    print(bold(f"\n[*] Target     : {green(base_url)}"))
    print(bold(f"[*] Wordlist   : {cyan(os.path.basename(wl_path))} ({len(words)} words)"))
    print(bold(f"[*] Extensions : {yellow(args.extensions if args.extensions else 'none')}"))
    print(bold(f"[*] Threads    : {args.threads}"))
    print(bold(f"[*] Status     : {args.status}"))
    print(bold(f"[*] Total Reqs : {total_words}"))
    print(bold(f"[*] Started    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
    print(cyan("\n" + "─" * 60))
    print(green("[+] FOUND PATHS:"))
    print(cyan("─" * 60 + "\n"))

    # Build queue
    q = Queue()
    for word in words:
        q.put(word)

    start_time = time.time()

    # Start progress thread
    progress_thread = threading.Thread(target=show_progress, args=(total_words, start_time), daemon=True)
    progress_thread.start()

    # Start scanner threads
    threads = []
    for _ in range(min(args.threads, len(words))):
        t = threading.Thread(target=scanner, args=(q, base_url, extensions, args.timeout, status_codes, args.output, session))
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    stop_event.set()
    elapsed = time.time() - start_time

    # Summary
    print(f"\n\n{cyan('─' * 60)}")
    print(bold(f"\n[*] Scan Complete!"))
    print(bold(f"[*] Time Elapsed  : {elapsed:.2f} seconds"))
    print(bold(f"[*] Total Scanned : {scanned_count}"))
    print(bold(f"[*] Paths Found   : {green(str(len(found_paths)))}"))
    if args.output:
        print(bold(f"[*] Results saved : {args.output}"))
    print()

if __name__ == "__main__":
    main()
