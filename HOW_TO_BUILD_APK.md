# 🚀 How to Build Your APK - Complete Instructions

## ❌ Why APK Can't Be Built Here

The APK **cannot be built in this environment** because:
- No Android Studio installed
- No Android SDK available
- No Gradle build tools
- Container has limited capabilities

## ✅ How to Build APK on Your Computer

### 📦 **What You Have**

A complete Android project ready to build:
- Location: `/app/android/` folder
- Size: ~22 KB (compressed)
- All files configured and ready

---

## 🎯 METHOD 1: Build in Android Studio (Easiest)

### Step 1: Download the Android Project

You have two options:

**Option A: Download from Emergent (if available)**
- Use the Emergent platform's download feature
- Download the entire `/app` folder
- Extract to your computer

**Option B: Copy the folder manually**
- Copy the `/app/android` folder to your local machine
- Put it anywhere (Desktop, Documents, etc.)

### Step 2: Install Android Studio

**Download:** https://developer.android.com/studio

**Windows:**
1. Run installer
2. Choose "Standard" installation
3. Wait for SDK download (10-15 min)

**Mac:**
1. Download .dmg
2. Drag to Applications
3. Open and follow setup

### Step 3: Update MainActivity.java

**File location:** `android/app/src/main/java/com/mpumpcalc/MainActivity.java`

**Line 28 - Change URL:**
```java
private static final String APP_URL = "https://muro-alpha.vercel.app";
```

**To your deployed URL:**
```java
private static final String APP_URL = "https://YOUR-VERCEL-URL.vercel.app";
```

### Step 4: Update SDK Path

**File location:** `android/local.properties`

**Find your Android SDK path:**
1. Open Android Studio
2. File → Settings → Android SDK
3. Copy the SDK path shown

**Update the file:**
```properties
sdk.dir=C:\\Users\\YourName\\AppData\\Local\\Android\\Sdk
```
(Use double backslashes on Windows)

### Step 5: Open Project

1. Launch Android Studio
2. Click "Open"
3. Select the `android` folder
4. Wait for Gradle sync (5-10 min first time)

### Step 6: Build APK

**For Testing (Debug APK):**
1. Build → Build Bundle(s) / APK(s) → Build APK(s)
2. Wait 1-3 minutes
3. Click "locate" when done

**APK Location:**
```
android/app/build/outputs/apk/debug/app-debug.apk
```

### Step 7: Install on Phone

1. Transfer APK to phone
2. Enable "Install from Unknown Sources"
3. Tap APK to install

---

## 🎯 METHOD 2: Build via Command Line

### Prerequisites

You need installed:
- Android SDK
- Gradle
- JDK 11+

### Commands

```bash
# Navigate to android folder
cd android

# Make gradlew executable (Mac/Linux)
chmod +x gradlew

# Build Debug APK
./gradlew assembleDebug

# Build Release APK (requires signing)
./gradlew assembleRelease

# Find APK
ls -la app/build/outputs/apk/debug/
```

**On Windows:**
```cmd
cd android
gradlew.bat assembleDebug
```

---

## 🎯 METHOD 3: Online Build Services

### Option A: GitHub Actions (FREE)

1. Push android folder to GitHub
2. Create `.github/workflows/build.yml`
3. GitHub builds APK automatically
4. Download from Actions tab

**Build file example:**
```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-java@v2
        with:
          java-version: '11'
      - name: Build APK
        run: |
          cd android
          chmod +x gradlew
          ./gradlew assembleDebug
      - uses: actions/upload-artifact@v2
        with:
          name: app-debug
          path: android/app/build/outputs/apk/debug/app-debug.apk
```

### Option B: AppCenter (FREE)

1. Sign up: https://appcenter.ms
2. Create new Android app
3. Connect repository
4. Configure build
5. Download APK

---

## 📋 Pre-Build Checklist

Before building, make sure:

- [ ] Updated `APP_URL` in MainActivity.java
- [ ] Updated `sdk.dir` in local.properties
- [ ] Android Studio installed
- [ ] Gradle sync completed
- [ ] No errors in Build tab

---

## 🎨 Optional Customizations

### Change App Name
**File:** `android/app/src/main/res/values/strings.xml`
```xml
<string name="app_name">Your App Name</string>
```

### Change App Icon
1. Right-click `res` folder in Android Studio
2. New → Image Asset
3. Upload your 512x512 PNG icon
4. Finish

### Change Package Name
**File:** `android/app/build.gradle`
```gradle
applicationId "com.yourcompany.yourapp"
```

Also update in:
- AndroidManifest.xml
- MainActivity.java package line
- Folder structure

### Change Version
**File:** `android/app/build.gradle`
```gradle
versionCode 2        // Increment for each release
versionName "1.1.0"  // Semantic version
```

---

## 🐛 Common Issues & Solutions

### "Gradle sync failed"
**Solution:**
```
File → Invalidate Caches / Restart
File → Sync Project with Gradle Files
```

### "SDK not found"
**Solution:**
Update `local.properties` with correct SDK path

### "BUILD FAILED"
**Check:**
1. Internet connection (downloads dependencies)
2. Disk space (needs ~5 GB)
3. Java version (needs JDK 11+)
4. Gradle version (uses 8.2)

### "Unable to start daemon process"
**Solution:**
Close Android Studio and delete:
- Windows: `C:\Users\YourName\.gradle\caches\`
- Mac: `~/.gradle/caches/`
- Restart Android Studio

---

## 📦 APK Details

**Generated APK:**
- **Debug APK:** app-debug.apk (~8-15 MB)
- **Release APK:** app-release.apk (~5-10 MB, optimized)

**What's included:**
- WebView with your web app
- LocalStorage support
- PDF download capability
- File access permissions
- Back button navigation
- Portrait orientation locked

---

## 🚀 After Building APK

### Test on Multiple Devices

Recommended test devices:
- Low-end Android (Android 7.0)
- Mid-range Android (Android 10)
- High-end Android (Android 14)

### Test These Features:

✅ App launches
✅ Loads web app
✅ Data persists (close/reopen)
✅ PDF download works
✅ Back button navigation
✅ Permissions granted
✅ No crashes

### Distribution Options

**1. Direct Distribution (FREE):**
- Share APK file
- Users enable "Install from Unknown Sources"
- Install APK

**2. Google Play Store ($25 one-time):**
- Better for wider distribution
- Automatic updates
- User trust
- Payment processing

---

## 💾 Backup Important Files

Before distributing, save these:

1. **Keystore file** (if you created release APK)
   - `mpump-release-key.jks`
   - Password written down
   - You need this for ALL future updates!

2. **APK file**
   - Keep a copy of each version
   - Name them with version: `mpump-v1.0.apk`

3. **Source code**
   - Keep the entire `android` folder
   - Version control with Git (recommended)

---

## 📞 Need Help?

**Read these guides:**
1. `/app/android/STEP_BY_STEP_GUIDE.md` - Detailed walkthrough
2. `/app/android/README.md` - Technical documentation
3. `/app/android/QUICKSTART.md` - Quick reference

**Online resources:**
- Android Studio: https://developer.android.com/studio
- Build APK guide: https://developer.android.com/studio/build
- Stack Overflow: Search your error

---

## ⚡ Quick Command Reference

**Build APK:**
```bash
cd android
./gradlew assembleDebug
```

**Clean build:**
```bash
./gradlew clean
```

**Install on connected device:**
```bash
./gradlew installDebug
```

**Generate signed release:**
```bash
./gradlew assembleRelease
```

**List all tasks:**
```bash
./gradlew tasks
```

---

## 🎉 Summary

**To build APK, you need to:**

1. ✅ Download/Copy the `android` folder to your computer
2. ✅ Install Android Studio
3. ✅ Update APP_URL in MainActivity.java
4. ✅ Open project in Android Studio
5. ✅ Build → Build APK(s)
6. ✅ Find APK in `app/build/outputs/apk/debug/`
7. ✅ Install on phone and test

**Time required:** 
- First time: 30-45 minutes (including Android Studio installation)
- Subsequent builds: 2-5 minutes

Good luck with your APK! 🚀
