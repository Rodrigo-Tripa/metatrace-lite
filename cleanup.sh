#!/bin/bash

# cleanup.sh
# Removes contents of reports/ and samples/
# Asks whether tests/ should also be deleted (contents + folder)

set -e

REPORTS_DIR="reports"
SAMPLES_DIR="samples"
TESTS_DIR="tests"

echo "[*] MetaTrace Lite project cleanup"

# Clean reports/
if [ -d "$REPORTS_DIR" ]; then
    echo "[+] Cleaning contents of: $REPORTS_DIR/"
    rm -rf "${REPORTS_DIR:?}/"*
else
    echo "[-] Folder $REPORTS_DIR not found"
fi

# Clean samples/
if [ -d "$SAMPLES_DIR" ]; then
    echo "[+] Cleaning contents of: $SAMPLES_DIR/"
    rm -rf "${SAMPLES_DIR:?}/"*
else
    echo "[-] Folder $SAMPLES_DIR not found"
fi

# Ask about tests/
read -rp "[?] Do you want to completely remove the tests/ folder? (y/n): " choice

case "$choice" in
    y|Y|yes|YES)
        if [ -d "$TESTS_DIR" ]; then
            echo "[+] Removing folder: $TESTS_DIR/"
            rm -rf "$TESTS_DIR"
        else
            echo "[-] Folder $TESTS_DIR not found"
        fi
        ;;
    *)
        echo "[*] Keeping tests/ folder"
        ;;
esac

echo "[✓] Cleanup completed"