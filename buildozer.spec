[app]

# عنوان اپلیکیشن
title = SmartTranslateAi

# نام پکیج
package.name = smarttranslateai
package.domain = org.smarttranslate

# نسخه
version = 1.3.0

# دایرکتوری سورس
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ini

# ориентация
orientation = portrait

# نمایش کامل صفحه
fullscreen = 0

# مجوزهای اندروید
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# نسخه اندروید
android.api = 33
android.minapi = 24
android.ndk_api = 24

# وابستگی‌ها
requirements = python3,kivy==2.3.0,aiohttp,requests

# معماری
p4a.arch = arm64-v8a,armeabi-v7a

# تنظیمات Buildozer
[buildozer]
log_level = 2
warn_on_root = 1
buildozer.autoname = 1