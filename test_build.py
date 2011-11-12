#!/usr/bin/env python2.6
#coding=utf-8
#
# Copyright 2011, HUB Systems, Inc.
"""
UnitTest for "Build script for Android project".
"""
__author__ = "Koji Hasegawa"
__copyright__ = "Copyright 2011, HUB Systems, Inc."
__credits__ = ["Koji Hasegawa"]
__license__ = "Apache License Version 2.0"
__version__ = "1.0"

import unittest
import os
import shutil
from build import *


class BuildTests(unittest.TestCase):

    def test_manifest_read_0_8_3_7(self):
        """通常のManifestファイルの読み込みテスト"""
        try:
            shutil.copyfile('testing/AndroidManifest_0.8.3.7.xml', 'AndroidManifest.xml')
            manifest = Manifest()
            assert manifest.versionName == "0.8.3"
            assert manifest.versionCode == "7"
            assert manifest.debuggable == True
        finally:
            #tear down
            os.remove('AndroidManifest.xml')

    def test_manifest_read_0_9_0_0(self):
        """VersionNameが2桁、VersionCodeなし、debuggableがfalseのケース"""
        try:
            shutil.copyfile('testing/AndroidManifest_0.9.0.0.xml', 'AndroidManifest.xml')
            manifest = Manifest()
            assert manifest.versionName == "0.9.0"
            assert manifest.versionCode == "0"
            assert manifest.debuggable == False
        finally:
            #tear down
            os.remove('AndroidManifest.xml')

    def test_manifest_read_1_0_0_0(self):
        """VersionNameが1桁、VersionCodeなし、debuggableなしのケース"""
        try:
            shutil.copyfile('testing/AndroidManifest_1.0.0.0.xml', 'AndroidManifest.xml')
            manifest = Manifest()
            assert manifest.versionName == "1.0.0"
            assert manifest.versionCode == "0"
            assert manifest.debuggable == False
        finally:
            #tear down
            os.remove('AndroidManifest.xml')

    def test_manifest_write_normal(self):
        """書き込みテスト。versioncode, debuggableがある場合"""
        try:
            shutil.copyfile('testing/AndroidManifest_0.8.3.7.xml', 'AndroidManifest.xml')
            manifest = Manifest()
            #chnge value
            manifest.versionName = "0.8.4"
            manifest.versionCode = "8"
            manifest.debuggable = False
            manifest.write()
            #reload for test
            manifest = Manifest()
            assert manifest.versionName == "0.8.3"  # Do NOT overwrite.
            assert manifest.versionCode == "8"
            assert manifest.debuggable == False
        finally:
            #tear down
            os.remove('AndroidManifest.xml')

    def test_manifest_write_no_attributes(self):
        """書き込みテスト。versioncode, debuggableがない場合"""
        try:
            shutil.copyfile('testing/AndroidManifest_1.0.0.0.xml', 'AndroidManifest.xml')
            manifest = Manifest()
            #chnge value
            manifest.versionName = "1.1"
            manifest.versionCode = "1"
            manifest.debuggable = False
            manifest.write()
            #reload for test
            manifest = Manifest()
            assert manifest.versionName == "1.0.0"  # Do NOT overwrite.
            #元がないので置換されない assert manifest.versionCode == "1"
            #元がないので置換されない assert manifest.debuggable == False
        finally:
            #tear down
            os.remove('AndroidManifest.xml')

    def test_buildVersion_read(self):
        """build.versionファイルの読み込みテスト"""
        try:
            shutil.copyfile('testing/build.version', 'build.version')
            buildVersion = BuildVersion()
            assert buildVersion.version == "11"
        finally:
            #tear down
            os.remove('build.version')

    def test_buildVersion_no_file(self):
        """build.versionファイルが無い場合のテスト"""
        buildVersion = BuildVersion()
        assert buildVersion.version == "0"

    def test_buildVersion_write(self):
        """build.versionファイルの書き込みテスト"""
        try:
            shutil.copyfile('testing/build.version', 'build.version')
            buildVersion = BuildVersion()
            buildVersion.version = "12"
            buildVersion.write()
            #reload for test
            buildVersion = BuildVersion()
            assert buildVersion.version == "12"
        finally:
            #tear down
            os.remove('build.version')

    def test_buildXml_read(self):
        """build.xmlファイルの読み込みテスト"""
        try:
            shutil.copyfile('testing/build.xml', 'build.xml')
            buildXml = BuildXml()
            assert buildXml.projectName == "sunlightyellowmushroom"
        finally:
            #tear down
            os.remove('build.xml')

    def test_copyright_read_2010(self):
        """copyrightファイルの読み込みテスト. toは現在年に上書きされる"""
        try:
            os.mkdir('res')
            os.mkdir('res/values')
            shutil.copyfile('testing/copyright_2010.xml', 'res/values/copyright.xml')
            copyright = Copyright()
            copyright.update(2011)
            copyright.write()
            #reload for test
            copyright = Copyright()
            assert copyright.copyright_year_from == 2010
            assert copyright.copyright_year_to == 2011
        finally:
            #tear down
            shutil.rmtree('res')

    def test_copyright_read_2012(self):
        """copyrightファイルの読み込みテスト. to>現在年のときは上書きしない"""
        try:
            os.mkdir('res')
            os.mkdir('res/values')
            shutil.copyfile('testing/copyright_2012.xml', 'res/values/copyright.xml')
            copyright = Copyright()
            copyright.update(2011)
            copyright.write()
            #reload for test
            copyright = Copyright()
            assert copyright.copyright_year_from == 2010
            assert copyright.copyright_year_to == 2012
        finally:
            #tear down
            shutil.rmtree('res')

    def test_copyright_no_file(self):
        """copyrightファイルが無い場合、新規作成される"""
        try:
            os.mkdir('res')
            os.mkdir('res/values')
            copyright = Copyright()
            copyright.update(2011)
            copyright.write()
            #reload for test
            assert os.path.exists('res/values/copyright.xml')
            copyright = Copyright()
            assert copyright.copyright_year_from == 2011
            assert copyright.copyright_year_to == 2011
        finally:
            #tear down
            shutil.rmtree('res')

if __name__ == '__main__':
    unittest.main()
