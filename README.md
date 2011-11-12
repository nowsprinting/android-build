# Build script for Android project.


## Usage
    $ build.py
    Create .apk file following path "bin/<project.name>_<versionName>.<versionCode>.apk"

    If "build.xml" file is not exist, need run following command.
    $ android update project -p .

## Processing this script
    1. Update the "AndroidManifest.xml" file.
        1.1 Replace android:debuggable to "false".
        1.2 Increment android:versionCode.
    2. Create or update the "res/values/copyright.xml" file.
    3. Build project for release.
    4. Change the .apk file to "<project.name>_<versionName>.<versionCode>.apk"
    5. Update the "AndroidManifest.xml" file.
        5.1 Replace android:debuggable to "true".

## Cautions: This script create the following files.
    1. build.version
        This file is record the last "android:versionCode". You may wish to add to ".gitignore" file.
    2. res/values/copyright.xml
        You can use this file to the display of copyright in application.
        Do not modify this file -- YOUR CHANGES WILL BE ERASED!

