#!/bin/bash
# CV Crafter - One-Command Launcher
# Usage: ./run.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "🎯 CV Crafter - AI-Powered CV Generator"
echo "========================================"
echo ""

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ Python not found!${NC}"
        echo ""
        echo "Please install Python 3.10 or higher:"
        echo "  • macOS: brew install python3"
        echo "  • Or download from: https://www.python.org/downloads/"
        exit 1
    fi
    
    # Check version
    PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
    MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')
    
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
        echo -e "${RED}❌ Python $PYTHON_VERSION detected, but 3.10+ is required${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
}

# Setup virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}→ Creating virtual environment...${NC}"
        $PYTHON_CMD -m venv venv
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    else
        echo -e "${GREEN}✓ Virtual environment exists${NC}"
    fi
}

# Activate venv and install dependencies
install_deps() {
    source venv/bin/activate
    
    # Always sync dependencies (pip is fast when packages already installed)
    echo -e "${YELLOW}→ Checking dependencies...${NC}"
    pip install --upgrade pip -q 2>/dev/null
    pip install -r requirements.txt -q 2>/dev/null
    echo -e "${GREEN}✓ Dependencies ready${NC}"
}

# Create data directory if needed
setup_data() {
    if [ ! -d "data" ]; then
        mkdir -p data
    fi
}

# Run the app
run_app() {
    echo ""
    echo -e "${GREEN}🚀 Starting CV Crafter...${NC}"
    echo -e "   Opening in your browser at ${YELLOW}http://localhost:8501${NC}"
    echo -e "   Press ${YELLOW}Ctrl+C${NC} to stop"
    echo ""
    
    streamlit run app.py --server.headless=true
}

# Main
check_python
setup_venv
install_deps
setup_data
run_app
