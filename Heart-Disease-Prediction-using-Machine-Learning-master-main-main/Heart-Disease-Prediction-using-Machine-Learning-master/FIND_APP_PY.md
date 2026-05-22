# 🔍 How to Find and Run app.py

## The Problem
You're getting "can't find app.py" because you're not in the correct directory.

## The Solution - Step by Step

### Step 1: Find Where You Are
In PyCharm Terminal, type:
```powershell
Get-Location
```

You'll see something like:
```
C:\Users\fidel\Downloads\Heart-Disease-Prediction-using-Machine-Learning-master-main
```

### Step 2: Find Where app.py Is
The `app.py` file is located at:
```
C:\Users\fidel\Downloads\Heart-Disease-Prediction-using-Machine-Learning-master-main\Heart-Disease-Prediction-using-Machine-Learning-master\app.py
```

Notice it's **one level deeper** than where you probably are!

### Step 3: Navigate to the Correct Folder
Type this command:
```powershell
cd "Heart-Disease-Prediction-using-Machine-Learning-master"
```

### Step 4: Verify You're in the Right Place
Check that `app.py` is there:
```powershell
Test-Path app.py
```

Should return: `True`

Or see all files:
```powershell
Get-ChildItem
```

You should see `app.py` in the list!

### Step 5: Run the App
Now run:
```powershell
python -m streamlit run app.py
```

## 🎯 Quick Visual Guide

```
Your Project Structure:
└── Heart-Disease-Prediction-using-Machine-Learning-master-main/  ← You might be here
    └── Heart-Disease-Prediction-using-Machine-Learning-master/   ← You need to be HERE
        ├── app.py  ← The file you need!
        ├── heart.csv
        ├── run_streamlit.py
        └── ... other files
```

## ✅ Alternative: Use the Helper Script

Instead of navigating, you can:

1. **In PyCharm**, right-click on `check_path.py`
2. Select **Run 'check_path'**
3. It will show you exactly where `app.py` is and how to get there

Or:

1. **In PyCharm**, right-click on `run_streamlit.py`
2. Select **Run 'run_streamlit'**
3. It will automatically find and run `app.py`

## 🚀 Even Easier: Double-Click Method

1. Navigate to the folder in Windows File Explorer:
   ```
   C:\Users\fidel\Downloads\Heart-Disease-Prediction-using-Machine-Learning-master-main\Heart-Disease-Prediction-using-Machine-Learning-master
   ```

2. Double-click `run_app.bat`
3. The app will start automatically!

