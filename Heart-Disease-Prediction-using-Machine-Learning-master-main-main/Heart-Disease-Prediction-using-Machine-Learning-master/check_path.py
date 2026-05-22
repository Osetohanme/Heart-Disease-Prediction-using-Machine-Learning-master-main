"""
Quick script to check if app.py exists and show the correct path
Run this in PyCharm to see where app.py is located
"""

import os

print("=" * 60)
print("Checking for app.py...")
print("=" * 60)

# Current directory
current_dir = os.getcwd()
print(f"\n📍 Current directory: {current_dir}")

# Check if app.py is in current directory
app_path = os.path.join(current_dir, "app.py")
if os.path.exists(app_path):
    print(f"✅ Found app.py in current directory!")
    print(f"   Path: {app_path}")
else:
    print("❌ app.py NOT found in current directory")
    
    # Search in subdirectories
    print("\n🔍 Searching in subdirectories...")
    found = False
    for root, dirs, files in os.walk(current_dir):
        if 'app.py' in files:
            full_path = os.path.join(root, 'app.py')
            rel_path = os.path.relpath(full_path, current_dir)
            print(f"✅ Found app.py at:")
            print(f"   Full path: {full_path}")
            print(f"   Relative path: {rel_path}")
            print(f"\n💡 To navigate there, run:")
            print(f"   cd \"{os.path.dirname(rel_path)}\"")
            found = True
            break
    
    if not found:
        print("❌ app.py not found anywhere in subdirectories!")
        print("\n📁 Current directory contents:")
        try:
            items = os.listdir(current_dir)
            for item in items[:10]:  # Show first 10 items
                item_path = os.path.join(current_dir, item)
                item_type = "📁" if os.path.isdir(item_path) else "📄"
                print(f"   {item_type} {item}")
        except Exception as e:
            print(f"   Error listing directory: {e}")

print("\n" + "=" * 60)

