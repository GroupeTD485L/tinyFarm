#!/bin/bash
set -e  # Stop if any command fails

# Ensure SDKMAN is loaded before using it
#source ~/.sdkman/bin/sdkman-init.sh

# Install Java
#sdk install java 17.0.8-tem

# Install Playwright and Chromium browser
pip install playwright
playwright install chromium
