#!/bin/bash
# Logout from all ACP agents
# Removes credentials and tokens using native logout commands where available

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=== ACP Agent Logout Script ==="
echo ""

# Function to run CLI logout command
cli_logout() {
    local name="$1"
    local cmd="$2"

    if command -v "$(echo "$cmd" | awk '{print $1}')" &> /dev/null; then
        if eval "$cmd" 2>/dev/null; then
            echo -e "${GREEN}[✓]${NC} $name: Logged out via CLI"
        else
            echo -e "${YELLOW}[~]${NC} $name: CLI logout failed or not logged in"
        fi
    else
        echo -e "${YELLOW}[~]${NC} $name: CLI not installed"
    fi
}

# Function to remove credential file
remove_file() {
    local name="$1"
    local path="$2"

    if [ -e "$path" ]; then
        rm -rf "$path"
        echo -e "${GREEN}[✓]${NC} $name: Removed $path"
    else
        echo -e "${YELLOW}[~]${NC} $name: $path not found"
    fi
}

echo "--- CLI-based logout ---"

# Auggie
cli_logout "auggie" "auggie logout"

# Claude Code
cli_logout "claude" "claude /logout"

# Codex
cli_logout "codex" "codex logout"

echo ""
echo "--- File-based logout ---"

# Gemini
remove_file "gemini" "$HOME/.gemini/.oauth_creds.json"

# Mistral Vibe
remove_file "mistral-vibe" "$HOME/.vibe/.env"

# Goose
remove_file "goose" "$HOME/.config/goose/config.yaml"

# Kimi
remove_file "kimi" "$HOME/.kimi"

# Qwen Code
remove_file "qwen-code" "$HOME/.qwen/.env"

# Stakpak
remove_file "stakpak" "$HOME/.stakpak"

# Code Assistant
remove_file "code-assistant" "$HOME/.config/code-assistant/providers.json"

# Docker cagent
remove_file "cagent" "$HOME/.config/cagent"

echo ""
echo -e "${YELLOW}[!]${NC} opencode: Run 'opencode auth logout' manually (interactive)"
echo ""
echo -e "${GREEN}=== Logout complete ===${NC}"