#!/usr/bin/env bash
# ModelScope deployment setup: install system dependencies for CJK PDF support.
set -e

if [ -f /etc/debian_version ]; then
    echo "📦 Installing CJK fonts for PDF generation..."
    apt-get update -qq
    apt-get install -y -qq fonts-noto-cjk 2>/dev/null || \
        apt-get install -y -qq fonts-wqy-microhei 2>/dev/null || \
        echo "⚠️  Could not install CJK fonts. Chinese text in PDF may not render correctly."
    echo "✅ System dependencies installed."
else
    echo "⚠️  Not a Debian-based system. Skipping system font installation."
fi
