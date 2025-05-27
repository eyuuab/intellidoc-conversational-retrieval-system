#!/usr/bin/env python3
"""
IntelliDoc Streamlit Application Runner

This script provides a convenient way to run the IntelliDoc Streamlit application
with proper environment setup and configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'plotly',
        'pandas',
        'sentence_transformers',
        'chromadb',
        'langchain',
        'fastapi'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def setup_environment():
    """Setup environment variables"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("⚠️  .env file not found. Creating from template...")
        
        # Create .env from .env.example if it exists
        example_file = Path(".env.example")
        if example_file.exists():
            with open(example_file, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file from template")
        else:
            # Create basic .env file
            with open(env_file, 'w') as f:
                f.write("""# IntelliDoc Environment Configuration
HOST=127.0.0.1
PORT=8001
CHROMA_DB_PATH=chroma_data
EMBEDDING_MODEL=all-MiniLM-L6-v2
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=pdf,txt
DEBUG=True
RELOAD=True

# Add your Google API key here for full functionality
# GOOGLE_API_KEY=your_api_key_here
""")
            print("✅ Created basic .env file")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️  python-dotenv not installed, skipping .env loading")

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting IntelliDoc Streamlit Application...")
    print("📱 The app will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        return False
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it with: pip install streamlit")
        return False
    
    return True

def main():
    """Main function"""
    print("🔧 IntelliDoc Streamlit Runner")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("streamlit_app.py").exists():
        print("❌ streamlit_app.py not found!")
        print("💡 Make sure you're running this from the project root directory")
        return 1
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        return 1
    
    # Setup environment
    print("🔧 Setting up environment...")
    setup_environment()
    
    # Run the application
    if not run_streamlit():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
