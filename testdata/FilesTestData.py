#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012-2021 Smartling, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this work except in compliance with the License.
 * You may obtain a copy of the License in the LICENSE file, or at:
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limit
"""

from builder.Parameters import Code
from builder.ExampleData import TestData

testsOrder = [
    'uploadSourceFile',
    'downloadSourceFile',
    'getFileTranslationStatusAllLocales',
    'getFileTranslationStatusSingleLocale',
    'downloadTranslatedFileSingleLocale',
    'downloadTranslatedFilesAllLocales',
    'downloadMultipleTranslatedFiles',
    'getRecentlyUploadedSourceFilesList',
    'getFileTypesList',
    'renameUploadedSourceFile',
    'getTranslatedFileLastModifiedDateSingleLocale',
    'getTranslatedFileLastModifiedDateAllLocales',
    'importFileTranslations',
    'exportFileTranslations',
    'getRecentlyPublishedFilesList',
    'deleteUploadedSourceFile',
]

teardown = '''
        res, status = self.files_api.deleteUploadedSourceFile(self.uri16)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)

        res, status = self.files_api.deleteUploadedSourceFile(self.uri_json)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
'''

imports = '''
from smartlingApiSdk.Constants import FileTypes
from datetime import date
import zipfile
if isPython3:
    import io
else:
    import StringIO

if isPython3:
    newline = b"\\n"
else:
    newline = "\\n"
'''

extraInitializations = '''
        self.extraInitializations()

    def extraInitializations(self):
        self.FILE_NAME = "java.properties"
        self.FILE_NAME_16 = "javaUTF16.properties"
        self.FILE_TYPE = "javaProperties"
        self.FILE_TYPE_CSV = "csv"
        self.FILE_PATH = smartlingApiSdk.__path__[0]+"/resources/"
        self.FILE_NAME_NEW = "java.properties.renamed"
        self.FILE_NAME_NEW_16 = "javaUTF16.properties.renamed"
        self.FILE_NAME_CSV = "test.csv"
    
        self.FILE_NAME_IMPORT_ORIG = "test_import.xml"
        self.FILE_NAME_IMPORT_TRANSLATED = "test_import_es.xml"
        self.FILE_TYPE_IMPORT = "android"

        self.CALLBACK_URL = "http://google.com/?q=hello"

        unique_suffix = "_" + repr(time.time())
        self.uri = self.FILE_NAME + unique_suffix 
        self.uri16 = self.FILE_NAME_16 + unique_suffix 
        res, status = self.files_api.uploadSourceFile(self.FILE_PATH + self.FILE_NAME_16, fileType=self.FILE_TYPE, fileUri = self.uri16, localeIdsToAuthorize = [self.MY_LOCALE] )
        
        self.uri_to_rename = self.FILE_NAME_NEW + unique_suffix
        self.uri_import = self.FILE_NAME_IMPORT_ORIG + unique_suffix

        self.file_json = "simple.json"
        self.uri_json = unique_suffix + self.file_json
        res, status = self.files_api.uploadSourceFile(self.FILE_PATH + self.file_json, fileType="json", fileUri=self.uri_json, localeIdsToAuthorize = [self.MY_LOCALE] )

    def getZipFile(self, res):
        if isPython3:
            return zipfile.ZipFile(io.BytesIO(res))
        else:
            return zipfile.ZipFile(StringIO.StringIO(res))
'''

testEnvironment = 'stg'

testDecorators = {
    'uploadSourceFile':TestData(
        {
            "file":Code('self.FILE_PATH + self.FILE_NAME'),
            "fileUri" : Code('self.uri'),
            "fileType" : Code('self.FILE_TYPE'),
            'localeIdsToAuthorize' : Code('[self.MY_LOCALE]'),
        },
        customTestCheck='''
assert_equal(res.data.wordCount, 6)
assert_equal(res.data.stringCount, 6)
'''
    ),

    'deleteUploadedSourceFile' : TestData(
        {
            'fileUri' :  Code('self.uri')
        }
    ),

    'downloadSourceFile' : TestData(
        {
            'fileUri' :  Code('self.uri_json')
        },
        customTestCheck='''
orig = open(self.FILE_PATH + self.file_json , "rb").read()
assert_equal(res, orig)
''',
        isApiV2Response= False,
    ),

    'getFileTranslationStatusAllLocales': TestData(
        {
            'fileUri' :  Code('self.uri')
        },
        customTestCheck='''
assert_equal(res.data.fileUri, self.uri)
assert_equal(True, len(res.data.items) > 0)
'''
    ),

    'getFileTranslationStatusSingleLocale': TestData(
        {
            'fileUri' :  Code('self.uri'),
            'localeId' : Code('self.MY_LOCALE')
        },
        customTestCheck='''
assert_equal(res.data.fileUri, self.uri)
assert_equal(res.data.fileType, self.FILE_TYPE)
'''
    ),

    'downloadTranslatedFileSingleLocale':  TestData(
        {
            'fileUri' :  Code('self.uri'),
            'localeId' : Code('self.MY_LOCALE')
        },
        customTestCheck='''
resp_lines_count = len(res.decode('utf-8').split('\\n'))
file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME, "rb").read().decode('utf-8').split('\\n') )
assert_equal(resp_lines_count, file_lines_count)
''',
        isApiV2Response= False,
    ),

    'downloadTranslatedFilesAllLocales' : TestData(
        {
            'fileUri' :  Code('self.uri'),
        },
        customTestCheck='''
zfile = self.getZipFile(res)
names = zfile.namelist()
assert_equal(True, self.MY_LOCALE+'/'+self.uri in names)
''',
        isApiV2Response= False,
    ),

    'downloadMultipleTranslatedFiles' : TestData(
        {
            'fileUris' : Code('[self.uri,self.uri16]'),
            'localeIds': Code("[self.MY_LOCALE, 'zh-TW']"),
        },
        customTestCheck='''
zfile = self.getZipFile(res)
names = zfile.namelist()
assert_equal(True, self.MY_LOCALE+'/'+self.uri in names)
assert_equal(True, self.MY_LOCALE+'/'+self.uri16 in names)
assert_equal(True, 'zh-TW'+'/'+self.uri in names)
assert_equal(True, 'zh-TW'+'/'+self.uri16 in names)
''',
        isApiV2Response= False,
    ),

    'getRecentlyUploadedSourceFilesList' : TestData(
        {
            'fileTypes' : Code('[FileTypes.android, FileTypes.javaProperties]')
        },
        customTestCheck='''
uris = [x['fileUri'] for x in res.data.items]
assert_equal(True, self.uri in uris)
assert_equal(True, self.uri16 in uris)
'''
    ),

    'getFileTypesList' : TestData(
        {
        },
        customTestCheck='''
assert_equal(True, "javaProperties" in res.data.items)
'''
    ),

    'renameUploadedSourceFile' : TestData(
        {
            'fileUri' :  Code('self.uri'),
            'newFileUri' :  Code('self.uri_to_rename'),

        },
        customTestCheck='''
res, status = self.files_api.renameUploadedSourceFile(self.uri_to_rename, self.uri) #rename it back so in the end it could be removed
'''
    ),


    'getTranslatedFileLastModifiedDateSingleLocale' : TestData(
        {
            'fileUri' :  Code('self.uri'),
            'localeId' : Code('self.MY_LOCALE')

        },
        customTestCheck='''
lm_date = res.data.lastModified[:10]
assert_equal(lm_date,  date.today().isoformat())
'''
    ),

    'getTranslatedFileLastModifiedDateAllLocales' : TestData(
        {
            'fileUri' :  Code('self.uri'),

        },
        customTestCheck='''
assert_equal(True, len(res.data.items) > 0)
for l in res.data.items:
    if l['localeId'] == self.MY_LOCALE:
        lm_date = l['lastModified'][:10]
        assert_equal(lm_date,  date.today().isoformat())
'''
    ),

    'importFileTranslations' : TestData(
        {
            'fileUri' :  Code('self.uri_import'),
            'localeId' : Code('self.MY_LOCALE'),
            'file' : Code('self.FILE_PATH + self.FILE_NAME_IMPORT_TRANSLATED'),
            'fileType' : Code('self.FILE_TYPE_IMPORT'),
            'translationState' : 'PUBLISHED',
        },
        ['res, status = self.files_api.uploadSourceFile(self.FILE_PATH + self.FILE_NAME_IMPORT_ORIG, fileType = self.FILE_TYPE_IMPORT , fileUri=self.uri_import)'],
        customTestCheck='''

assert_equal(res.data.wordCount, 2)
assert_equal(res.data.stringCount, 2)
assert_equal(res.data.translationImportErrors, [])

res, status = self.files_api.deleteUploadedSourceFile(self.uri_import)
assert_equal(200, status)
assert_equal(self.CODE_SUCCESS_TOKEN, res.code)

'''
    ),

    'exportFileTranslations' : TestData(
        {
            'fileUri' :  Code('self.uri'),
            'localeId' : Code('self.MY_LOCALE'),
            'file' : Code('self.FILE_PATH+self.FILE_NAME'),
        },
        customTestCheck='''
assert_equal(True, res is not None)
resp_lines_count = len(res.split(newline))
file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME, "rb").readlines() )
assert_equal(resp_lines_count, file_lines_count)
''',
        isApiV2Response= False,
    ),

    'getRecentlyPublishedFilesList' : TestData(
        {
            'publishedAfter': Code('datetime.datetime.fromtimestamp(time.time()-10*24*2600).strftime("%Y-%m-%d")'),
            'localeIds' :  Code('[self.MY_LOCALE]'),
        },
        customTestCheck='''
assert_equal(True, hasattr(res.data, 'items'))
'''
    ),


}

