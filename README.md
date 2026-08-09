# Voice Translator APK - Build Instructions

## Prerequisites (on Linux build machine)

```bash
# Install buildozer and dependencies
pip install buildozer cython

# System dependencies (Ubuntu/Debian)
sudo apt update && sudo apt install -y \
    git zip unzip openjdk-17-jdk python3-pip \
    build-essential libsqlite3-dev libffi-dev \
    libssl-dev libjpeg-dev zlib1g-dev \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly gstreamer1.0-libav \
    gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa \
    gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio
```

## Build the APK

```bash
cd voice_translator_apk

# First build (downloads NDK, SDK, compiles everything - takes 30-60 min)
buildozer -v android debug

# Subsequent builds are faster
buildozer android debug
```

## Output

APK will be in `bin/` directory:
```
bin/voicetranslator-1.0.0-arm64-v8a-debug.apk
bin/voicetranslator-1.0.0-armeabi-v7a-debug.apk
```

## Install on Device

```bash
# Via ADB
adb install bin/voicetranslator-1.0.0-arm64-v8a-debug.apk

# Or transfer APK to phone and install manually
```

## Known Issues & Fixes

### 1. Vosk compilation fails
If vosk fails to build, add to `buildozer.spec`:
```ini
# Use pre-built vosk wheels
p4a.extra_args = --require=vosk
```

Or build vosk separately and include native libs:
```ini
android.add_libs_arm64_v8a = /path/to/libvosk.so
android.add_libs_armeabi_v7a = /path/to/libvosk.so
```

### 2. PyAudio compilation fails
```ini
# In buildozer.spec
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1
```

### 3. Model files too large for APK
Models (Vosk ~40MB, Argos ~300MB) exceed APK size limits. Options:
- **Download on first run** (recommended) - app downloads models from GitHub
- **Split APK** - use Android App Bundle (AAB)
- **External storage** - prompt user to download

### 4. Permissions
App requests:
- RECORD_AUDIO
- INTERNET (for Google STT fallback, model downloads)
- READ/WRITE_EXTERNAL_STORAGE (for model caching)
- FOREGROUND_SERVICE (for background listening)

## Alternative: Chaquopy (Android Studio)

If buildozer fails, use **Chaquopy** with Android Studio - better native support:

```gradle
// build.gradle (project)
dependencies {
    classpath "com.chaquo.python:gradle:14.0.0"
}

// build.gradle (app)
apply plugin: "com.chaquo.python"

python {
    buildPython "3.11"
    pip {
        install "vosk==0.3.45"
        install "argostranslate==1.11.0"
        install "SpeechRecognition==3.17.0"
        install "pyaudio==0.2.14"
        install "numpy==1.26.0"
    }
}
```

## Testing Locally (before building)

```bash
# Test on Linux
pip install -r requirements.txt
python3 main.py
```

## File Structure

```
voice_translator_apk/
├── buildozer.spec      # Build configuration
├── main.py             # Kivy app entry point
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Notes

- **First build takes 30-60 minutes** (downloads NDK, SDK, compiles Python + native libs)
- **APK size ~80-150MB** depending on included models
- **Vosk model auto-downloads** on first run if not bundled
- **Argos model auto-downloads** on first run
- **Internet required** for first run (model downloads) and Google STT fallback
- **Android 5.0+ (API 21)** minimum

## Troubleshooting

Check build logs:
```bash
buildozer -v android debug 2>&1 | tee build.log
```

Common fixes in `buildozer.spec`:
- Increase `android.minapi` if targeting newer Android
- Add `android.gradle_wrapper = True` for gradle wrapper
- Set `android.aab = True` for Play Store (generates .aab instead of .apk)