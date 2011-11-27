#!/usr/bin/env python2.6
#coding=utf-8
#
# Copyright 2011, HUB Systems, Inc.
"""
Build script for Android project.

Usage
    $ build.py
    Create .apk file following path "bin/<project.name>_<versionName>.<versionCode>.apk"

    If "build.xml" file is not exist, need run following command.
    $ android update project -p .

Processing this script
    1. Update the "AndroidManifest.xml" file.
        1.1 Replace android:debuggable to "false".
        1.2 Increment android:versionCode.
    2. Create or update the "res/values/copyright.xml" file.
    3. Build project for release.
    4. Rename .apk file to "<project.name>_<versionName>.<versionCode>.apk"
    5. Update the "AndroidManifest.xml" file.
        5.1 Replace android:debuggable to "true".

Cautions: This script create the following files.
    1. build.version
        This file is record the last "android:versionCode".
        You may wish to add to ".gitignore" file.
    2. res/values/copyright.xml
        You can use this file to the display of copyright in application.
        Do not modify this file -- YOUR CHANGES WILL BE ERASED!

"""
__author__ = "Koji Hasegawa"
__copyright__ = "Copyright 2011, HUB Systems, Inc."
__credits__ = ["Koji Hasegawa"]
__license__ = "Apache License Version 2.0"
__version__ = "1.0"

import shutil
import os
import re
from xml.dom.minidom import parse, parseString
from subprocess import check_call
from datetime import datetime

TEMP_FILE = '/var/tmp/buildtemp.xml'


class Manifest:
    """AndroidManifest.xml file accessor.
        read/write proerties: versionName, versionCode, debuggable."""
    _FILE_PATH      = 'AndroidManifest.xml'
    _VERSION_NAME   = 'android:versionName'
    _VERSION_CODE   = 'android:versionCode'
    _DEBUGGABLE     = 'android:debuggable'

    def __init__(self):
        xml = parse(self._FILE_PATH)
        manifest = xml.getElementsByTagName('manifest')[0]
        self.versionName = manifest.getAttribute(self._VERSION_NAME) if manifest.hasAttribute(self._VERSION_NAME) else "1.0.0"
        while re.search('\d+\.\d+\.\d+', self.versionName)==None:
            self.versionName = self.versionName + ".0"
        self.versionCode = manifest.getAttribute(self._VERSION_CODE) if manifest.hasAttribute(self._VERSION_CODE) else "0"
        application = manifest.getElementsByTagName('application')[0]
        if application.hasAttribute(self._DEBUGGABLE):
            self.debuggable = True if application.getAttribute(self._DEBUGGABLE).lower()=="true" else False
        else:
            self.debuggable = False
        xml.unlink()

    def write(self):
        try:
            read = open(self._FILE_PATH, 'r')
            temp = open(TEMP_FILE, 'w')
            for line in read:
                line = re.sub(self._VERSION_CODE+'="\d+"', self._VERSION_CODE+'="'+self.versionCode+'"', line)
                line = re.sub(self._DEBUGGABLE+'="\w+"',   self._DEBUGGABLE + '="'+str(bool(self.debuggable)).lower()+'"', line)
                temp.write(line)
        finally:
            read.close()
            temp.close()
        shutil.move(TEMP_FILE, self._FILE_PATH)


class BuildVersion:
    """buldl.version file accessor.
        read/write property: version."""
    _FILE_PATH = 'build.version'

    def __init__(self):
        self.version = '0'
        read = None
        try:
            read = open(self._FILE_PATH, 'r')
            for line in read:
                matched = re.search('(\d+)', line)
                if matched:
                    self.version = matched.group(1)
                    break
        except (IOError,OSError):
            pass
        finally:
            if read:
                read.close()

    def write(self):
        try:
            fp = open(self._FILE_PATH, 'w')
            fp.write(self.version+'\n')
        finally:
            fp.close()


class BuildXml:
    """buldl.xml file accessor.
        read property: projectName."""
    _FILE_PATH = 'build.xml'

    def __init__(self):
        xml = parse(self._FILE_PATH)
        project = xml.getElementsByTagName('project')[0]
        self.projectName = project.getAttribute('name')
        xml.unlink()


class Copyright:
    """copyright.xml file accessor.
        read/write profile: copyright_year_from, copyright_year_to."""
    _FILE_PATH = 'res/values/copyright.xml'
    copyright_year_from = 0
    copyright_year_to   = 0

    def __init__(self):
        xml = None
        try:
            xml = parse(self._FILE_PATH)
            resources = xml.getElementsByTagName('resources')[0]
            strings = resources.getElementsByTagName('string')
            for current in strings:
                currentName = current.getAttribute('name')
                if currentName=='copyright_year_from':
                    self.copyright_year_from = int(current.childNodes[0].data)
                if currentName=='copyright_year_to':
                    self.copyright_year_to = int(current.childNodes[0].data)
        except (IOError,OSError):
            pass
        finally:
            if xml:
                xml.unlink()

    def update(self, year):
        if self.copyright_year_from==0:
            self.copyright_year_from = year
        if self.copyright_year_to<year:
            self.copyright_year_to = year

    def write(self):
        fp = None
        try:
            fp = open(self._FILE_PATH, 'w')
            fp.write('<?xml version="1.0" encoding="utf-8"?>\n')
            fp.write('<resources>\n')
            fp.write('    <string name="copyright_year_from">' + str(self.copyright_year_from) + '</string>\n')
            fp.write('    <string name="copyright_year_to">' + str(self.copyright_year_to) + '</string>\n')
            fp.write('</resources>\n')
        except (IOError,OSError):
            pass
        finally:
            if fp:
                fp.close()


def increment_and_set_BuildVersion(manifest, build_version):
    """Of the two parameters, to set as the "Build version" to the number+1, whichever is greater."""
    version_code_from_manifest = int(manifest.versionCode)
    version_code_from_buildver = int(build_version.version)
    if version_code_from_manifest>version_code_from_buildver:
        version_code_from_manifest += 1
        manifest.versionCode  = str(version_code_from_manifest)
        build_version.version = str(version_code_from_manifest)
    else:
        version_code_from_buildver += 1
        manifest.versionCode  = str(version_code_from_buildver)
        build_version.version = str(version_code_from_buildver)


if __name__ == '__main__':
    manifest = Manifest()
    build_version = BuildVersion()
    build_xml = BuildXml()
    copyright = Copyright()

    # Pre build.
    increment_and_set_BuildVersion(manifest, build_version)
    manifest.debuggable = False
    manifest.write()
    build_version.write()
    copyright.update(datetime.today().year)
    copyright.write()

    # Do build.
    check_call(["ant", "release"])

    # Rename apk file.
    shutil.move('bin/'+build_xml.projectName+'-release.apk',
            'bin/'+build_xml.projectName+'_'+manifest.versionName+'.'+manifest.versionCode+'.apk')

    # After build.
    manifest.debuggable = True
    manifest.write()
