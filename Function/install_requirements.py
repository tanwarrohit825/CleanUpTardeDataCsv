import subprocess
import sys
import os

def install_requirements():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "-r", "requirements.txt"], check=True)
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error installing dependencies:", e)

    # Restart kernel (for Jupyter or interactive environments)
    print("Restarting kernel...")
    os._exit(00)

if __name__ == "__main__":
    install_requirements()
