#!/usr/bin/env python3
"""
CV Crafter - Cross-platform launcher
Run with: python start.py (or python3 start.py)
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print()
    print("🎯 CV Crafter - AI-Powered CV Generator")
    print("=" * 40)
    print()
    
    # Check Python version
    if sys.version_info < (3, 10):
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} detected")
        print("   Python 3.10 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Setup venv
    venv_dir = script_dir / "venv"
    
    if sys.platform == "win32":
        python_path = venv_dir / "Scripts" / "python.exe"
        pip_path = venv_dir / "Scripts" / "pip.exe"
    else:
        python_path = venv_dir / "bin" / "python"
        pip_path = venv_dir / "bin" / "pip"
    
    if not venv_dir.exists():
        print("→ Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment exists")
    
    # Install dependencies
    print("→ Checking dependencies...")
    subprocess.run(
        [str(pip_path), "install", "-q", "--upgrade", "pip"],
        capture_output=True
    )
    result = subprocess.run(
        [str(pip_path), "install", "-q", "-r", "requirements.txt"],
        capture_output=True
    )
    if result.returncode != 0:
        print("→ Installing dependencies (this may take a minute)...")
        subprocess.run(
            [str(pip_path), "install", "-r", "requirements.txt"],
            check=True
        )
    print("✓ Dependencies ready")
    
    # Create data directory
    data_dir = script_dir / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Run streamlit
    print()
    print("🚀 Starting CV Crafter...")
    print("   Opening in your browser at http://localhost:8501")
    print("   Press Ctrl+C to stop")
    print()
    
    try:
        subprocess.run(
            [str(python_path), "-m", "streamlit", "run", "app.py", "--server.headless=true"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 CV Crafter stopped. Goodbye!")

if __name__ == "__main__":
    main()
