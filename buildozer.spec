[app]

title = Gacha Impact
package.name = gachaimpact
package.domain = fr.noni78

# Build from the existing Python game at the repository root.
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,json,mp4,gif
source.exclude_dirs = .git,.github,.vscode,__pycache__,mobile,unused,bin,.buildozer

version = 1.0.1

# Native package: original Pygame/OpenCV source only; the discarded web prototype is excluded.
# Keep the original Pygame/OpenCV implementation and its video playback code.
requirements = python3==3.11.5,hostpython3==3.11.5,pygame,opencv

# The existing game was designed for a 16:9 desktop layout.
orientation = landscape
fullscreen = 1

# SDL2 is the Android backend. Pin p4a so recipe and toolchain versions stay reproducible.
p4a.bootstrap = sdl2
p4a.branch = develop
p4a.commit = 1c9a4b4f817847bd8505d972d1a0e6f965929a88
p4a.local_recipes = ./p4a-recipes

android.api = 35
android.minapi = 24
android.ndk = 28c
android.archs = arm64-v8a
android.accept_sdk_license = True
android.release_artifact = apk
android.debug_artifact = apk

# Build settings
log_level = 2
warn_on_root = 1
