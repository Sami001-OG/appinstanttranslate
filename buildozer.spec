[app]

# (str) Title of your application
title = Voice Translator

# (str) Package name
package.name = voicetranslator

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,model,onnx,spm

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,vosk,argostranslate,SpeechRecognition,pyaudio,numpy,librosa,soundfile,requests

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source = /path/to/local/folder

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# (str) Entry point of the application
main.py = main.py

#
# OSX Specific
#

# (str) Path to the OSX icon
#osx.icon = %(source.dir)s/icon.icns

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (str) Android API to use
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
#android.sdk = 33

# (str) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK path (if custom)
#android.ndk_path =

# (str) Android SDK path (if custom)
#android.sdk_path =

# (str) Android JRE path (if custom)
#android.jre_path =

# (str) Android gradle path (if custom)
#android.gradle_path =

# (str) Android gradle version to use
#android.gradle_version = 8.0

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid any internet access for the build
#android.skip_sdk_update = False

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android entry point
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# Use that to provide a custom manifest, or to add custom permissions
#android.manifest_extra = <uses-permission android:name="android.permission.RECORD_AUDIO"/>

# (list) Permissions
android.permissions = RECORD_AUDIO,INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE

# (int) Target Android API, should be as high as possible.
#android.targetapi = 33

# (list) Permissions to add at runtime
#android.permissions_runtime =

# (list) Android features to add to manifest
#android.features = android.hardware.microphone

# (str) Python-for-android branch to use
#p4a.branch = master

# (str) Python-for-android git clone url (if using custom)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your build
#p4a.build_dir =

# (bool) If True, then skip trying to update python-for-android
#p4a.skip_update = False

# (list) Extra arguments to pass to python-for-android toolchain
#p4a.extra_args =

# (bool) If True, disable automatic generation of __pycache__ directories
#p4a.skip_pycache = False

# (str) Architecture to build for
android.archs = arm64-v8a,armeabi-v7a

# (int) The Android API level to target for multidex
#android.multidex = False

# (str) Bundle identifier (package name for iOS)
#ios.bundle_id = org.example.voicetranslator

# (str) Path to the icon file for iOS
#ios.icon = %(source.dir)s/icon.png

# (str) Path to the launch image for iOS
#ios.launch_image = %(source.dir)s/launch.png

# (str) Supported interface orientations for iOS
#ios.orientations = Portrait,PortraitUpsideDown

# (bool) If True, use the iOS app extensions
#ios.enable_extensions = False

# (list) Extra frameworks for iOS
#ios.frameworks =

# (list) Extra libraries for iOS
#ios.libraries =

# (bool) If True, build the iOS app in release mode
#ios.release = False

# (list) Arguments to pass to the iOS codesign command
#ios.codesign_args =

# (bool) If True, use the iOS simulator
#ios.simulator = False

# (str) Additional arguments to pass to the codesign command
#ios.codesign_identity = iPhone Developer

# (str) Python version to use
#python.version = 3.11

# (str) The Android package to use as a base for the app
#android.base_package = org.kivy.android

# (list) List of Java dependencies to include
#android.gradle_dependencies =

# (list) List of additional aar files to include
#android.add_aars =

# (list) List of additional jars to include
#android.add_jars =

# (list) List of additional native libs to include for arm64-v8a
#android.add_libs_arm64_v8a =

# (list) List of additional native libs to include for armeabi-v7a
#android.add_libs_armeabi_v7a =

# (bool) Enable AndroidX
android.enable_androidx = True

# (bool) Use old toolchain (for compatibility)
#android.use_old_toolchain = False

# (str) Android TV support
#android.tv = False

# (str) Android Wear support
#android.wear = False

# (list) Permissions to remove from manifest
#android.remove_permissions =

# (str) Custom build template
#android.build_template =

# (bool) Build in debug mode
debug = True

# (str) Name of the certificate to use for signing the debug version
#android.debug.keystore =

# (str) Password for the debug keystore
#android.debug.keystore_password =

# (str) Alias for the debug keystore
#android.debug.keyalias =

# (str) Password for the debug key
#android.debug.keypass =

# (str) Name of the certificate to use for signing the release version
#android.release.keystore =

# (str) Password for the release keystore
#android.release.keystore_password =

# (str) Alias for the release keystore
#android.release.keyalias =

# (str) Password for the release key
#android.release.keypass =

# (str) Format of the apk filename
#android.release_artifact = %(app_name)s-%(version)s-%(android.arch)s-%(mode)s.apk

# (bool) If True, then sign the release APK
#android.release.sign = True

# (str) The name of the launcher activity
#android.launcher_activity = org.kivy.android.PythonActivity

# (list) List of services to run at startup
#services =

# (str) The name of the file that contains the app version code
#android.version_code_file =

# (int) Version code for the app (auto-increment if not specified)
#android.version_code = 1

# (str) Custom keystore properties file
#android.keystore_properties =

# (bool) If True, use the new app bundle format (aab)
#android.aab = False

# (str) Application class name
#android.app_class = org.kivy.android.PythonApplication

# (list) Extra arguments for the build
#android.extra_args =

# (str) Path to the gradle wrapper
#android.gradle_wrapper = gradlew

# (bool) If True, use the gradle wrapper
android.gradle_wrapper = True

# (str) Path to the proguard file
#android.proguard =

# (bool) If True, enable proguard
#android.proguard_enabled = False

# (str) The name of the property file for the version
#android.version_property =

# (bool) If True, use the new Android App Bundle format
android.aab = False

# (list) List of additional native libraries to include
#android.add_libs =

# (str) The minimum OpenGL ES version required
#android.gl_es_version = 2

# (list) List of supported ABIs
#android.abis =

# (bool) If True, build with multi-dex
#android.multidex = False

# (list) List of native libraries to bundle
#android.native_libs =

# (bool) If True, use the Python shared library
#android.use_python_shared = False

# (str) The path to the Python shared library
#android.python_shared_lib =

# (bool) If True, strip the native libraries
android.strip = True

# (list) List of additional CFLAGS
#android.cflags =

# (list) List of additional LDFLAGS
#android.ldflags =

# (str) The name of the Python library to use
#android.python_lib = python3.11

# (bool) If True, use the system Python
#android.use_system_python = False

# (list) List of additional packages to include in the APK
#android.extra_packages =

# (bool) If True, include the Python standard library
#android.include_stdlib = True

# (list) List of Python packages to exclude
#android.exclude_packages =

# (list) List of additional files to include
#android.extra_files =

# (list) List of directories to include
#android.extra_dirs =

# (str) Path to the custom Python-for-android distribution
#p4a.distribution =

# (bool) If True, use the custom distribution
#p4a.custom_distribution = False

# (str) The name of the custom distribution
#p4a.dist_name =

# (str) The path to the custom distribution
#p4a.dist_path =

# (list) List of recipes to include
#p4a.recipes =

# (list) List of recipes to exclude
#p4a.exclude_recipes =

# (str) The name of the bootstrap
#p4a.bootstrap = sdl2

# (bool) If True, use the new bootstrap
#p4a.new_bootstrap = False

# (str) The name of the bootstrap module
#p4a.bootstrap_module =

# (bool) If True, use the new bootstrap
#p4a.new_bootstrap = False

# (list) List of additional build requirements
#build.requirements =

# (list) List of additional build dependencies
#build.deps =

# (str) The name of the build tool
#build.tool =

# (str) The path to the build tool
#build.tool_path =

# (bool) If True, use the local build
#build.local = False

# (str) The name of the build directory
#build.dir = .buildozer

# (bool) If True, clean the build directory
#build.clean = False

# (bool) If True, force rebuild
#build.force = False

# (str) The name of the log file
#build.log = build.log

# (bool) If True, show verbose output
#build.verbose = False

# (bool) If True, show debug output
#build.debug = False

# (str) The name of the output file
#build.output =

# (bool) If True, keep the build directory
#build.keep = False

# (bool) If True, use the cache
#build.cache = True

# (str) The path to the cache directory
#build.cache_dir =

# (bool) If True, use the parallel build
#build.parallel = True

# (int) Number of parallel jobs
#build.jobs = 4

# (bool) If True, use the incremental build
#build.incremental = True

# (str) The name of the incremental build file
#build.incremental_file =

# (bool) If True, use the incremental build
#build.incremental = True