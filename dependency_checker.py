import importlib
import sys
import subprocess

def check_dependencies():
    """Checks for required ML project dependencies and suggests installations."""
    print("🔍 Starting Dependency Check...\n")
    
    # Map of module name to pip package name
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'openpyxl': 'openpyxl',
        'joblib': 'joblib',
        'folium': 'folium',
        'flask': 'flask',
        'flask_cors': 'flask-cors',
        'googlemaps': 'googlemaps',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn'
    }
    
    missing_packages = []
    
    for module, pip_name in required_packages.items():
        try:
            importlib.import_module(module)
            print(f"✅ {module} is installed.")
        except ImportError:
            print(f"❌ {module} is missing.")
            missing_packages.append(pip_name)
            
    print("\n--- Summary ---")
    if not missing_packages:
        print("🎉 All required dependencies are already installed. You are ready to run the project!")
    else:
        print(f"⚠️ Found {len(missing_packages)} missing dependencies.")
        install_command = f"{sys.executable} -m pip install " + " ".join(missing_packages)
        print("\nRun the following command to install ONLY the missing packages:")
        print(f"\n   {install_command}\n")
        
        # Optionally, autorun
        # subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)

if __name__ == "__main__":
    check_dependencies()
