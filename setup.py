"""
Setup script for the AI Image Generator
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True

def setup_env_file():
    """Setup environment file"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("Creating .env file...")
        with open(env_file, "w") as f:
            f.write("# Add your OpenAI API key here\n")
            f.write("OPENAI_API_KEY=your_api_key_here\n")
        print("✓ .env file created. Please edit it and add your OpenAI API key.")
    else:
        print("✓ .env file already exists.")

def main():
    print("=== AI Image Generator Setup ===")
    
    # Install requirements
    if not install_requirements():
        return
    
    # Setup environment file
    setup_env_file()
    
    print("\n=== Setup Complete ===")
    print("Next steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Run: python main.py")
    print("\nEnjoy generating pixelated images!")

if __name__ == "__main__":
    main()
