# 🔍 DarkBuster

> Advanced Web Directory & File Bruteforcer with Updated Wordlists (May 2026)

![Python](https://img.shields.io/badge/Python-3.6+-blue?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Wordlists](https://img.shields.io/badge/Wordlists-Updated%20May%202026-orange?style=flat)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Kali-red?style=flat&logo=linux)
![Author](https://img.shields.io/badge/Author-darkdisaster08-purple?style=flat)

---

## ⚠️ Disclaimer

> **DarkBuster is intended for authorized security testing and educational purposes only.**
> Always obtain explicit written permission before testing any system you do not own.
> Unauthorized use against systems you don't own is illegal and unethical.
> The author is not responsible for any misuse or damage caused by this tool.

---

## 🌟 Features

- ✅ **Updated Wordlists** — Curated and updated up to May 2026
- ✅ **Multi-threaded** — Fast scanning with configurable thread count
- ✅ **Multiple Wordlists** — Common, Admin panels, API endpoints, Backups, Technology-specific
- ✅ **Extension Support** — Append file extensions (.php, .html, .bak etc.)
- ✅ **Color-coded Output** — Easy to read results by status code
- ✅ **Save Results** — Export findings to file
- ✅ **Custom Headers** — User-agent, cookies support
- ✅ **Progress Display** — Real-time scan progress and ETA
- ✅ **Safe & Stable** — No crashes, handles all errors gracefully
- ✅ **Easy to Use** — Simple CLI interface for all skill levels

---

## 📦 Installation

### Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/darkdisaster08/darkbuster.git
cd darkbuster

# Run installer
chmod +x install.sh
./install.sh
```

### Manual Install

```bash
git clone https://github.com/darkdisaster08/darkbuster.git
cd darkbuster
pip3 install -r requirements.txt
python3 darkbuster.py --help
```

### Kali Linux

```bash
git clone https://github.com/darkdisaster08/darkbuster.git
cd darkbuster
pip3 install requests
python3 darkbuster.py -u http://target.com
```

---

## 🚀 Usage

### Basic Scan

```bash
python3 darkbuster.py -u http://target.com
```

### Scan with Extensions

```bash
python3 darkbuster.py -u http://target.com -x .php,.html,.bak
```

### Use Specific Wordlist

```bash
python3 darkbuster.py -u http://target.com -w wordlists/admin-panels.txt
```

### Fast Scan with More Threads

```bash
python3 darkbuster.py -u http://target.com -t 50
```

### Save Results to File

```bash
python3 darkbuster.py -u http://target.com -o results.txt
```

### HTTPS with Cookie

```bash
python3 darkbuster.py -u https://target.com --cookie "session=abc123"
```

### Full Options

```bash
python3 darkbuster.py -u http://target.com -w wordlists/common.txt -x .php,.html -t 30 -o output.txt
```

### List All Available Wordlists

```bash
python3 darkbuster.py --list-wordlists
```

---

## ⚙️ Options

| Flag | Description | Default |
|------|-------------|---------|
| `-u, --url` | Target URL | Required |
| `-w, --wordlist` | Wordlist file | common.txt |
| `-t, --threads` | Thread count | 20 |
| `-x, --extensions` | Extensions to test | None |
| `-o, --output` | Save results to file | None |
| `-s, --status` | Status codes to show | 200,301,302,307,401,403 |
| `--timeout` | Request timeout (seconds) | 5 |
| `--user-agent` | Custom User-Agent | DarkBuster/1.0 |
| `--cookie` | Cookie header | None |
| `--list-wordlists` | Show available wordlists | - |

---

## 📚 Wordlists

All wordlists are updated to **May 2026** and carefully curated for real-world pentesting.

| Wordlist | Entries | Description |
|----------|---------|-------------|
| `common.txt` | 300+ | Most common web directories and files |
| `admin-panels.txt` | 110+ | Admin panel paths across all major CMS |
| `api-endpoints.txt` | 120+ | REST API and GraphQL endpoints |
| `backup-files.txt` | 130+ | Backup and sensitive file names |
| `subdomains.txt` | 100+ | Common subdomain names |
| `technology/wordpress.txt` | 40+ | WordPress specific paths |
| `technology/php.txt` | 60+ | PHP application files |

### What Makes These Wordlists Different?

- ✅ Cleaned and deduplicated
- ✅ Organized by category with comments
- ✅ Includes modern framework paths (Laravel, Next.js, etc.)
- ✅ Includes API and GraphQL endpoints
- ✅ Updated with paths discovered in recent bug bounties (2024-2026)
- ✅ Technology-specific lists for targeted scanning

---

## 🎯 Example Output

```
[200] http://target.com/admin (Size: 4521)
[301] http://target.com/backup → http://target.com/backup/ (Size: 0)
[403] http://target.com/.env (Size: 0)
[200] http://target.com/api/v1 (Size: 1203)
[401] http://target.com/admin/dashboard (Size: 512)

[*] Scan Complete!
[*] Time Elapsed  : 45.23 seconds
[*] Total Scanned : 1250
[*] Paths Found   : 5
```

---

## 🛡️ Status Code Reference

| Code | Color | Meaning |
|------|-------|---------|
| 200 | 🟢 Green | Found — accessible |
| 301/302 | 🟡 Yellow | Redirect — worth checking |
| 401 | 🔵 Cyan | Unauthorized — exists but needs auth |
| 403 | 🔴 Red | Forbidden — exists but blocked |

---

## 🔧 Tips for Best Results

1. **Start with common.txt** for a quick overview
2. **Add extensions** relevant to the target stack: `-x .php,.html` for PHP apps
3. **Use admin-panels.txt** specifically when looking for login pages
4. **Use api-endpoints.txt** for API testing
5. **Increase threads (-t 50)** on fast networks
6. **Save results (-o file.txt)** for documentation

---

## 📁 Repository Structure

```
darkbuster/
├── darkbuster.py           # Main tool
├── requirements.txt        # Dependencies
├── install.sh              # Quick installer
├── README.md               # Documentation
└── wordlists/
    ├── common.txt          # General purpose
    ├── admin-panels.txt    # Admin paths
    ├── api-endpoints.txt   # API endpoints
    ├── backup-files.txt    # Backup files
    ├── subdomains.txt      # Subdomain names
    └── technology/
        ├── wordpress.txt   # WordPress paths
        └── php.txt         # PHP files
```

---

## 🤝 Contributing

Contributions are welcome! Especially:
- New wordlist entries (with source/justification)
- Bug fixes
- Feature improvements
- New technology-specific wordlists

Please open an issue or pull request on GitHub.

---

## 📜 License

MIT License — see LICENSE file for details.

---

## 👤 Author

**Manjeet Thakur** (darkdisaster08)
- GitHub: [github.com/darkdisaster08](https://github.com/darkdisaster08)
- LinkedIn: [linkedin.com/in/manjeet-thakur-sec](https://linkedin.com/in/manjeet-thakur-sec)

---

## ⭐ Support

If DarkBuster helped you, please consider giving it a **star** ⭐ on GitHub!

*For authorized security testing only. Use responsibly.*
