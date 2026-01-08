import sys
import subprocess

print(f"Fixing Python environment: {sys.executable}")

# This command forces the CURRENT Python to install the package
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    print("\n✅ SUCCESS: python-dotenv installed successfully!")
    print("You can now run your original weather_api.py script.")
except Exception as e:
    print(f"\n❌ FAILED: {e}")