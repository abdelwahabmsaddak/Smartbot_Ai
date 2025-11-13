@echo off
title 🚀 SmartBot AI Runner
color 0a

echo ============================================
echo 🔍 Checking Python installation...
python --version 1>nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت على هذا الجهاز.
    echo 💡 قم بتحميله من https://www.python.org/downloads/
    pause
    exit /b
)
echo ✅ Python detected successfully.
echo ============================================

echo 📦 Installing dependencies from requirements.txt...
if exist requirements.txt (
    pip install -r requirements.txt > install_log.txt 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️ حدث خطأ أثناء تثبيت الحزم. راجع install_log.txt
        pause
        exit /b
    )
    echo ✅ Dependencies installed successfully.
) else (
    echo ⚠️ لم يتم العثور على ملف requirements.txt
)

echo ============================================
echo 🚀 Starting SmartBot AI Backend Server...
echo --------------------------------------------
python app.py > server_log.txt 2>&1

if %errorlevel% neq 0 (
    echo ❌ فشل في تشغيل الخادم. تحقق من server_log.txt
    pause
    exit /b
)

echo ✅ SmartBot AI server is running successfully!
echo 🌍 يمكنك الآن فتح المتصفح على:
echo 👉 http://127.0.0.1:5000
echo --------------------------------------------
pause
