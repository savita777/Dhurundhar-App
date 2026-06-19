# ─────────────────────────────────────────────────────────────────────────────
#  buildozer.spec  —  DHURANDHAR (2025)
#  Kivy text-adventure game  |  Bollywood Spy Universe
#  Agent: Hamza Ali Mazari   |  Codename: PHANTOM
#
#  How to build locally (after pip install buildozer):
#    buildozer android debug         ← debug APK for testing
#    buildozer android release       ← release APK (needs keystore)
#    buildozer android deploy run    ← push & run on connected device
# ─────────────────────────────────────────────────────────────────────────────

[app]

# ── Identity ──────────────────────────────────────────────────────────────────
title          = Dhurandhar 2025
package.name   = dhurandhar
package.domain = org.rawagent

# ── Source ────────────────────────────────────────────────────────────────────
source.dir           = .
source.include_exts  = py,png,jpg,jpeg,gif,kv,atlas,ttf,otf

# ── Version ───────────────────────────────────────────────────────────────────
version = 1.0.0

# ── Requirements ──────────────────────────────────────────────────────────────
# python3  → CPython for Android via p4a
# kivy     → latest stable Kivy (p4a recipe handles SDL2 automatically)
requirements = python3,kivy

# ── Orientation & Display ─────────────────────────────────────────────────────
orientation = portrait
fullscreen   = 1

# Splash screen background colour (hex, no #)
android.presplash_color = #070A14

# ── Permissions ───────────────────────────────────────────────────────────────
# INTERNET only — game has no file I/O, camera, or location needs
android.permissions = INTERNET

# ── Android SDK / NDK Targeting ───────────────────────────────────────────────
# Google Play requires targetSdkVersion >= 33 as of 2024
android.api     = 33
android.minapi  = 21          # Android 5.0 Lollipop+   (covers ~99 %% of devices)

# NDK 25b is the last version supported by all current p4a recipes
android.ndk     = 25b
android.ndk_api = 21

# Auto-accept the Android SDK licence during CI builds
android.accept_sdk_license = True

# Skip updating SDK on every build (speeds up CI; set False to always refresh)
android.skip_update = False

# ── ABI Targets ───────────────────────────────────────────────────────────────
# arm64-v8a  → modern 64-bit phones (required for Google Play since 2019)
# armeabi-v7a→ older 32-bit devices for maximum compatibility
android.archs = arm64-v8a, armeabi-v7a

# ── Android Entry Point ───────────────────────────────────────────────────────
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme   = "@android:style/Theme.NoTitleBar"

# Allow Android auto-backup (Google's cloud save for app data)
android.allow_backup = True

# ── iOS (placeholder — not configured) ───────────────────────────────────────
# ios.kivy_ios_url  = https://github.com/kivy/kivy-ios
# ios.kivy_ios_branch = master

# ── macOS desktop (placeholder) ───────────────────────────────────────────────
# osx.python_version = 3
# osx.kivy_version   = 2.3.0

[buildozer]

# 0 = errors only | 1 = info | 2 = full debug with command output
log_level = 2

# Warn (don't block) if buildozer is run as root
warn_on_root = 1
