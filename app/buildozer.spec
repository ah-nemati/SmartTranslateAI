name: SmartTranslateAi - Enterprise Build System

on:
  push:
    tags:
      - "v*"

permissions:
  contents: write

env:
  PYTHON_VERSION: "3.11"
  APP_NAME: SmartTranslateAi


jobs:

# ================= WINDOWS =================
  windows:
    runs-on: windows-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt pyinstaller

      - name: Build Windows EXE
        run: |
          pyinstaller --clean --onefile --windowed --name ${{ env.APP_NAME }} app/main.py

      - name: Upload Windows artifact
        uses: actions/upload-artifact@v4
        with:
          name: SmartTranslateAi-Windows
          path: dist/${{ env.APP_NAME }}.exe


# ================= LINUX =================
  linux:
    runs-on: ubuntu-24.04

    steps:
      - uses: actions/checkout@v4

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            libglib2.0-0 libgl1 libx11-6 libxext6 libxrender1 \
            libxcb1 libxcb-cursor0 libxkbcommon-x11-0 libdbus-1-3 \
            libnss3 libfontconfig1 libfreetype6 libegl1 libasound2t64

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt pyinstaller

      - name: Build Linux binary
        run: |
          pyinstaller --clean --onefile --windowed --name ${{ env.APP_NAME }} app/main.py

      - name: Upload Linux artifact
        uses: actions/upload-artifact@v4
        with:
          name: SmartTranslateAi-Linux
          path: dist/${{ env.APP_NAME }}


# ================= ANDROID (FIXED + STABLE) =================
  android:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y git zip unzip wget openjdk-17-jdk \
            build-essential libffi-dev libssl-dev

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip
          pip install buildozer cython kivy==2.3.0

      # ================= ANDROID SDK SETUP =================
      - name: Setup Android SDK
        run: |
          mkdir -p $HOME/android-sdk
          cd $HOME/android-sdk

          wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
          unzip commandlinetools-linux-*.zip

          mkdir -p cmdline-tools/latest
          mv cmdline-tools/* cmdline-tools/latest/ || true

          export ANDROID_HOME=$HOME/android-sdk
          export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH

          yes | sdkmanager --licenses || true

          sdkmanager "platform-tools" \
                     "platforms;android-33" \
                     "build-tools;33.0.2"

      # ================= BUILD CHECK =================
      - name: Verify buildozer.spec
        run: |
          if [ ! -f app/buildozer.spec ]; then
            echo "ERROR: buildozer.spec not found in app/"
            exit 1
          fi

      # ================= BUILD APK =================
      - name: Build Android APK
        run: |
          cd app
          buildozer -v android debug

      # ================= UPLOAD APK =================
      - name: Upload Android artifact
        uses: actions/upload-artifact@v4
        with:
          name: SmartTranslateAi-Android
          path: app/bin/*.apk


# ================= RELEASE =================
  release:
    needs: [windows, linux, android]
    runs-on: ubuntu-latest

    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts

      - name: Show artifacts
        run: ls -R artifacts

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: ${{ github.ref_name }}
          name: SmartTranslateAi ${{ github.ref_name }}
          generate_release_notes: true
          draft: false
          prerelease: false
          files: |
            artifacts/**/*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}