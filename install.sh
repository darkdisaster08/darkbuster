#!/bin/bash
# DarkBuster Installer
# GitHub: https://github.com/darkdisaster08

echo ""
echo "╔══════════════════════════════════════╗"
echo "║     DarkBuster Installer             ║"
echo "║     github.com/darkdisaster08        ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Please install Python3 first."
    exit 1
fi

echo "[*] Installing dependencies..."
python3 -m pip install -r requirements.txt --quiet --break-system-packages 2>/dev/null || \
python3 -m pip install -r requirements.txt --quiet

echo "[*] Setting permissions..."
chmod +x darkbuster.py

echo "[*] Creating symlink for global access..."
sudo ln -sf "$(pwd)/darkbuster.py" /usr/local/bin/darkbuster 2>/dev/null || \
    ln -sf "$(pwd)/darkbuster.py" ~/.local/bin/darkbuster 2>/dev/null

echo ""
echo "[✓] DarkBuster installed successfully!"
echo ""
echo "Usage Examples:"
echo "  darkbuster -u http://target.com"
echo "  darkbuster -u http://target.com -w wordlists/admin-panels.txt"
echo "  darkbuster -u http://target.com -x .php,.html -t 30"
echo "  darkbuster -u http://target.com -o results.txt"
echo "  darkbuster --list-wordlists"
echo ""
