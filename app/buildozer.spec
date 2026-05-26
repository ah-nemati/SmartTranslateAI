[app]

title = SmartTranslateAi
package.name = smarttranslateai
package.domain = org.smarttranslate

version = 1.5.3

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ini,json

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_NETWORK_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24
android.ndk_api = 24

requirements = python3,kivy==2.3.0,aiohttp

p4a.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1