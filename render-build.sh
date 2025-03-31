#!/usr/bin/env bash

echo "Installing Chrome & ChromeDriver..."

export INSTALL_DIR="/opt/render"
export CHROMEDRIVER_DIR="$INSTALL_DIR/chromedriver"
export CHROME_DIR="$INSTALL_DIR/chrome"

mkdir -p $CHROME_DIR
mkdir -p $CHROMEDRIVER_DIR

# Define latest Chrome version
CHROME_VERSION="134.0.6998.165"  # Update this dynamically if needed

# Install Chrome
wget -qO- "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" -O $CHROME_DIR/chrome.zip
unzip -o $CHROME_DIR/chrome.zip -d $CHROME_DIR/
export CHROME_BIN=$CHROME_DIR/chrome-linux64/chrome

# Verify Chrome installation
if [ ! -f "$CHROME_BIN" ]; then
    echo "❌ Chrome installation failed!"
    exit 1
fi

# Install ChromeDriver
wget "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" -O $CHROMEDRIVER_DIR/chromedriver.zip
unzip -o $CHROMEDRIVER_DIR/chromedriver.zip -d $CHROMEDRIVER_DIR/
chmod +x $CHROMEDRIVER_DIR/chromedriver

# Verify ChromeDriver installation
if [ ! -f "$CHROMEDRIVER_DIR/chromedriver" ]; then
    echo "❌ ChromeDriver installation failed!"
    exit 1
fi

echo "✅ Chrome and ChromeDriver installed successfully!"
