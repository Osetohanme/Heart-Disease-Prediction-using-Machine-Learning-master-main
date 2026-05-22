"""
Streamlit Launcher Script for PyCharm
This script helps run Streamlit when the 'streamlit' command is not recognized.
Simply run this file in PyCharm (right-click → Run 'run_streamlit')
"""

import subprocess
import sys
import os

def find_app_py():
    """Search for app.py in common locations"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check current directory
    app_path = os.path.join(script_dir, 'app.py')
    if os.path.exists(app_path):
        return script_dir, app_path
    
    # Check parent directory
    parent_dir = os.path.dirname(script_dir)
    app_path = os.path.join(parent_dir, 'app.py')
    if os.path.exists(app_path):
        return parent_dir, app_path
    
    # Search recursively in parent directory
    for root, dirs, files in os.walk(parent_dir):
        if 'app.py' in files:
            return root, os.path.join(root, 'app.py')
    
    return None, None

def main():
    # Find app.py
    app_dir, app_path = find_app_py()
    
    if app_dir is None:
        print("❌ Error: app.py not found!")
        print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")
        print("\n💡 Please make sure app.py exists in one of these locations:")
        print("   - Same directory as this script")
        print("   - Parent directory")
        print("   - Any subdirectory of the parent")
        print("\n🔍 Searching for app.py...")
        sys.exit(1)
    
    # Change to the directory containing app.py
    os.chdir(app_dir)
    
    print(f"✅ Found app.py at: {app_path}")
    
    print("🚀 Starting Streamlit app...")
    print(f"📁 Working directory: {app_dir}")
    print("🌐 The app will open in your browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the app\n")
    
    try:
        # Run streamlit using python -m streamlit (works even if streamlit command isn't in PATH)
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n✅ Streamlit app stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running Streamlit: {e}")
        print("\n💡 Try installing Streamlit:")
        print("   python -m pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

