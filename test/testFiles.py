
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
 * limitations under the License.
"""

import os
import sys
import time, datetime

sys.path += [os.path.abspath('../'), os.path.abspath('../../')]  # allow to import ../smartlingApiSdk.api

import smartlingApiSdk
from smartlingApiSdk.api.FilesApi import FilesApi
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

from smartlingApiSdk.Constants import FileTypes
from datetime import date
import zipfile
if isPython3:
    import io
else:
    import StringIO

if isPython3:
    newline = b"\n"
else:
    newline = "\n"

def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testFilesApi(object):

    CODE_SUCCESS_TOKEN = 'SUCCESS'
    ACCEPTED_TOKEN = 'ACCEPTED'

    def tearDown(self):
        print("tearDown", "OK")

    def setUp(self):
        credentials = Credentials('stg') #Gets your Smartling credetnials from environment variables
        self.MY_USER_IDENTIFIER = credentials.MY_USER_IDENTIFIER
        self.MY_USER_SECRET = credentials.MY_USER_SECRET
        self.MY_PROJECT_ID = credentials.MY_PROJECT_ID

        #needed for testProjects
        self.MY_ACCOUNT_UID = credentials.MY_ACCOUNT_UID
        self.MY_LOCALE = credentials.MY_LOCALE

        if self.MY_ACCOUNT_UID == "CHANGE_ME":
            print("can't test projects api call, set self.MY_ACCOUNT_UID or export SL_ACCOUNT_UID=*********")
            return

        useProxy = False
        if useProxy :
            proxySettings = ProxySettings("login", "password", "proxy_host", "proxy_port or None")
        else:
            proxySettings = None

        self.files_api = FilesApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

        print("setUp", "OK", "\n")

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

    def checkUploadSourceFile(self):
        """
            method  :  POST
            api url :  /files-api/v2/projects/{projectId}/file
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -F "file=@$uploadFilePath;type=text/plain" -F "fileUri=$uploadFileSmartlingUri" -F "fileType=$uploadFileSmartlingType" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file"
            Responses:
                200 : OK
                202 : ACCEPTED
                423 : The requested file is currently being processed by another operation. The file will be unlocked after the operation completes.
            details :  https://api-reference.smartling.com/#operation/uploadSourceFile
        """
        file=self.FILE_PATH + self.FILE_NAME
        fileUri=self.uri
        fileType=self.FILE_TYPE
        localeIdsToAuthorize=[self.MY_LOCALE]
        res, status = self.files_api.uploadSourceFile(file=file, fileUri=fileUri, fileType=fileType, localeIdsToAuthorize=localeIdsToAuthorize)


        assert_equal(res.data.wordCount, 6)
        assert_equal(res.data.stringCount, 6)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('uploadSourceFile', 'OK')


    def checkDownloadSourceFile(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/file
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G --data-urlencode "fileUri=$smartlingFileUri" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/downloadSourceFile
        """
        fileUri=self.uri_json
        res, status = self.files_api.downloadSourceFile(fileUri=fileUri)


        orig = open(self.FILE_PATH + self.file_json , "rb").read()
        assert_equal(res, orig)

        print('downloadSourceFile', 'OK')


    def checkGetFileTranslationStatusAllLocales(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/file/status
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getFileTranslationStatusAllLocales
        """
        fileUri=self.uri
        res, status = self.files_api.getFileTranslationStatusAllLocales(fileUri=fileUri)


        assert_equal(res.data.fileUri, self.uri)
        assert_equal(True, len(res.data.items) > 0)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getFileTranslationStatusAllLocales', 'OK')


    def checkGetFileTranslationStatusSingleLocale(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file/status
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getFileTranslationStatusSingleLocale
        """
        localeId=self.MY_LOCALE
        fileUri=self.uri
        res, status = self.files_api.getFileTranslationStatusSingleLocale(localeId=localeId, fileUri=fileUri)


        assert_equal(res.data.fileUri, self.uri)
        assert_equal(res.data.fileType, self.FILE_TYPE)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getFileTranslationStatusSingleLocale', 'OK')


    def checkDownloadTranslatedFileSingleLocale(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -o $smartlingLocaleId$smartlingFileUri -G --data-urlencode "fileUri=$smartlingFileUri" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/downloadTranslatedFileSingleLocale
        """
        localeId=self.MY_LOCALE
        fileUri=self.uri
        res, status = self.files_api.downloadTranslatedFileSingleLocale(localeId=localeId, fileUri=fileUri)


        resp_lines_count = len(res.decode('utf-8').split('\n'))
        file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME, "rb").read().decode('utf-8').split('\n') )
        assert_equal(resp_lines_count, file_lines_count)

        print('downloadTranslatedFileSingleLocale', 'OK')


    def checkDownloadTranslatedFilesAllLocales(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/locales/all/file/zip
            as curl :  curl -X GET -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/files-api/v2/projects/{projectId}/locales/all/file/zip?fileUri=yourfile.json&retrievalType=published'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/downloadTranslatedFilesAllLocales
        """
        fileUri=self.uri
        res, status = self.files_api.downloadTranslatedFilesAllLocales(fileUri=fileUri)


        zfile = self.getZipFile(res)
        names = zfile.namelist()
        assert_equal(True, self.MY_LOCALE+'/'+self.uri in names)

        print('downloadTranslatedFilesAllLocales', 'OK')


    def checkDownloadMultipleTranslatedFiles(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/files/zip
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/downloadMultipleTranslatedFiles
        """
        fileUris=[self.uri,self.uri16]
        localeIds=[self.MY_LOCALE, 'zh-TW']
        res, status = self.files_api.downloadMultipleTranslatedFiles(fileUris=fileUris, localeIds=localeIds)


        zfile = self.getZipFile(res)
        names = zfile.namelist()
        assert_equal(True, self.MY_LOCALE+'/'+self.uri in names)
        assert_equal(True, self.MY_LOCALE+'/'+self.uri16 in names)
        assert_equal(True, 'zh-TW'+'/'+self.uri in names)
        assert_equal(True, 'zh-TW'+'/'+self.uri16 in names)

        print('downloadMultipleTranslatedFiles', 'OK')


    def checkGetRecentlyUploadedSourceFilesList(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/files/list
            as curl :  curl -H "Authorization: Bearer $smartlingToken" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/files/list?fileTypes[]=json&uriMask=strings"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getRecentlyUploadedSourceFilesList
        """
        fileTypes=[FileTypes.android, FileTypes.javaProperties]
        res, status = self.files_api.getRecentlyUploadedSourceFilesList(fileTypes=fileTypes)


        uris = [x['fileUri'] for x in res.data.items]
        assert_equal(True, self.uri in uris)
        assert_equal(True, self.uri16 in uris)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getRecentlyUploadedSourceFilesList', 'OK')


    def checkGetFileTypesList(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/file-types
            as curl :  curl -H "Authorization: Bearer $smartlingToken" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file-types"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getFileTypesList
        """
        res, status = self.files_api.getFileTypesList()


        assert_equal(True, "javaProperties" in res.data.items)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getFileTypesList', 'OK')


    def checkRenameUploadedSourceFile(self):
        """
            method  :  POST
            api url :  /files-api/v2/projects/{projectId}/file/rename
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -F "fileUri=filename.properties" -F "newFileUri=filename2.properties" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file/rename'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/renameUploadedSourceFile
        """
        fileUri=self.uri
        newFileUri=self.uri_to_rename
        res, status = self.files_api.renameUploadedSourceFile(fileUri=fileUri, newFileUri=newFileUri)


        res, status = self.files_api.renameUploadedSourceFile(self.uri_to_rename, self.uri) #rename it back so in the end it could be removed

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('renameUploadedSourceFile', 'OK')


    def checkGetTranslatedFileLastModifiedDateSingleLocale(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file/last-modified
            as curl :  curl -X GET -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file/last-modified?fileUri=filename.properties'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getTranslatedFileLastModifiedDateSingleLocale
        """
        localeId=self.MY_LOCALE
        fileUri=self.uri
        res, status = self.files_api.getTranslatedFileLastModifiedDateSingleLocale(localeId=localeId, fileUri=fileUri)


        lm_date = res.data.lastModified[:10]
        assert_equal(lm_date,  date.today().isoformat())

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getTranslatedFileLastModifiedDateSingleLocale', 'OK')


    def checkGetTranslatedFileLastModifiedDateAllLocales(self):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/file/last-modified
            as curl :  curl -X GET -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file/last-modified?fileUri=filename.properties'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getTranslatedFileLastModifiedDateAllLocales
        """
        fileUri=self.uri
        res, status = self.files_api.getTranslatedFileLastModifiedDateAllLocales(fileUri=fileUri)


        assert_equal(True, len(res.data.items) > 0)
        for l in res.data.items:
            if l['localeId'] == self.MY_LOCALE:
                lm_date = l['lastModified'][:10]
                assert_equal(lm_date,  date.today().isoformat())

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getTranslatedFileLastModifiedDateAllLocales', 'OK')


    def checkImportFileTranslations(self):
        """
            method  :  POST
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file/import
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -F "file=@filename.properties" -F "fileUri=filename.properties" -F "fileType=javaProperties" -F "translationState=PUBLISHED" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file/import'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/importFileTranslations
        """
        res, status = self.files_api.uploadSourceFile(self.FILE_PATH + self.FILE_NAME_IMPORT_ORIG, fileType = self.FILE_TYPE_IMPORT , fileUri=self.uri_import)
        localeId=self.MY_LOCALE
        file=self.FILE_PATH + self.FILE_NAME_IMPORT_TRANSLATED
        fileUri=self.uri_import
        fileType=self.FILE_TYPE_IMPORT
        translationState='PUBLISHED'
        res, status = self.files_api.importFileTranslations(localeId=localeId, file=file, fileUri=fileUri, fileType=fileType, translationState=translationState)



        assert_equal(res.data.wordCount, 2)
        assert_equal(res.data.stringCount, 2)
        assert_equal(res.data.translationImportErrors, [])

        res, status = self.files_api.deleteUploadedSourceFile(self.uri_import)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)


        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('importFileTranslations', 'OK')


    def checkExportFileTranslations(self):
        """
            method  :  POST
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file/get-translations
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -F "file=@filename.properties" -F 'fileUri=filename.properties' 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file/get-translations'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/exportFileTranslations
        """
        localeId=self.MY_LOCALE
        file=self.FILE_PATH+self.FILE_NAME
        fileUri=self.uri
        res, status = self.files_api.exportFileTranslations(localeId=localeId, file=file, fileUri=fileUri)


        assert_equal(True, res is not None)
        resp_lines_count = len(res.split(newline))
        file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME, "rb").readlines() )
        assert_equal(resp_lines_count, file_lines_count)

        print('exportFileTranslations', 'OK')


    def checkGetRecentlyPublishedFilesList(self):
        """
            method  :  GET
            api url :  /published-files-api/v2/projects/{projectId}/files/list/recently-published
            as curl :  curl -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/published-files-api/v2/projects/$smartlingProjectId/files/list/recently-published?publishedAfter=2019-11-21T11:51:17Z&fileUris[]=files/example1.json&localeIds[]=fr-CA&limit=10&offset=100'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getRecentlyPublishedFilesList
        """
        publishedAfter=datetime.datetime.fromtimestamp(time.time()-10*24*2600).strftime("%Y-%m-%d")
        localeIds=[self.MY_LOCALE]
        res, status = self.files_api.getRecentlyPublishedFilesList(publishedAfter=publishedAfter, localeIds=localeIds)


        assert_equal(True, hasattr(res.data, 'items'))

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getRecentlyPublishedFilesList', 'OK')


    def checkDeleteUploadedSourceFile(self):
        """
            method  :  POST
            api url :  /files-api/v2/projects/{projectId}/file/delete
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -F "fileUri=filename.properties" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file/delete'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/deleteUploadedSourceFile
        """
        fileUri=self.uri
        res, status = self.files_api.deleteUploadedSourceFile(fileUri=fileUri)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('deleteUploadedSourceFile', 'OK')



    def test_all(self):
        t = self
        t.checkUploadSourceFile()
        t.checkDownloadSourceFile()
        t.checkGetFileTranslationStatusAllLocales()
        t.checkGetFileTranslationStatusSingleLocale()
        t.checkDownloadTranslatedFileSingleLocale()
        t.checkDownloadTranslatedFilesAllLocales()
        t.checkDownloadMultipleTranslatedFiles()
        t.checkGetRecentlyUploadedSourceFilesList()
        t.checkGetFileTypesList()
        t.checkRenameUploadedSourceFile()
        t.checkGetTranslatedFileLastModifiedDateSingleLocale()
        t.checkGetTranslatedFileLastModifiedDateAllLocales()
        t.checkImportFileTranslations()
        t.checkExportFileTranslations()
        t.checkGetRecentlyPublishedFilesList()
        t.checkDeleteUploadedSourceFile()
