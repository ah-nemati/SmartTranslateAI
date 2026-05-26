[app]

# =========================================================
# BASIC
# =========================================================
title = SmartTranslateAi

package.name = smarttranslateai
package.domain = org.smarttranslate

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ini,txt

version = 1.3.0

# =========================================================
# DISPLAY
# =========================================================
orientation = portrait
fullscreen = 0

# =========================================================
# REQUIREMENTS
# =========================================================
# Force downgrade to Python 3.11 to avoid C-API mismatch in Python 3.14
requirements = hostpython3==3.11.9, python3==3.11.9, kivy==2.3.0, aiohttp==3.11.11, pysrt, webvtt-py, python-dotenv

# =========================================================
# ANDROID
# =========================================================
android.api = 34
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.accept_sdk_license = True

# =========================================================
# PERMISSIONS
# =========================================================
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# =========================================================
# ARCHITECTURE
# =========================================================
android.archs = arm64-v8a

# =========================================================
# PERFORMANCE
# =========================================================
android.enable_androidx = True
android.allow_backup = True
android.release_artifact = apk

# =========================================================
# LOGGING
# =========================================================
log_level = 2

# =========================================================
# EXCLUDE FILES
# =========================================================
source.exclude_dirs = venv, env, .venv, .git, .github, __pycache__, tests, build, dist
source.exclude_patterns = *.spec, *.pyc, *.pyo

# =========================================================
# BUILD & KIVY & P4A
# =========================================================
warn_on_root = 1
osx.python_version = 3
osx.kivy_version = 2.3.0

p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1