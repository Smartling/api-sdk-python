
#!/usr/bin/python
# -*- coding: utf-8 -*-


''' Copyright 2012-2021 Smartling, Inc.
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
'''

import os
import sys
import time, datetime

lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from api.FilesApi import FilesApi
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

        self.api = FilesApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

        print("setUp", "OK", "\n")

        self.extraInitializations()

    def extraInitializations(self):
        self.FILE_NAME = "java.properties"
        self.FILE_NAME_16 = "javaUTF16.properties"
        self.FILE_TYPE = "javaProperties"
        self.FILE_TYPE_CSV = "csv"
        self.FILE_PATH = "../resources/"
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
        res, status = self.api.uploadSourceFile(self.FILE_PATH + self.FILE_NAME_16, fileType=self.FILE_TYPE, fileUri = self.uri16, localeIdsToAuthorize = [self.MY_LOCALE] )
        
        self.uri_to_rename = self.FILE_NAME_NEW + unique_suffix
        self.uri_import = self.FILE_NAME_IMPORT_ORIG + unique_suffix

    def getZipFile(self, res):
        if isPython3:
            return zipfile.ZipFile(io.BytesIO(res))
        else:
            return zipfile.ZipFile(StringIO.StringIO(res))

    def checkUploadSourceFile(self):
        """
            post
            /files-api/v2/projects/{projectId}/file
            for details check: https://api-reference.smartling.com/#operation/uploadSourceFile
            curl -X POST -H "Authorization: Bearer $smartlingToken" -F "file=@$uploadFilePath;type=text/plain" -F "fileUri=$uploadFileSmartlingUri" -F "fileType=$uploadFileSmartlingType" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file"

            ------------------------------------------------------------------------------------------------------------------------
            def commandUpload(self, filePath, fileType, directives={}, **kw):
                ''' https://developer.smartling.com/v1.0/reference#upload '''
                params = {
                        Params.FILE_URI: filePath,
                        Params.FILE_TYPE: fileType,
                        Params.FILE_PATH: filePath
                    }
        
                for k,v in list(kw.items()):
                    params[k] = v
        
                self.addLibIdDirective(params)
                self.processDirectives(params, directives)
        
                url = self.urlHelper.getUrl(self.urlHelper.UPLOAD)
                return self.uploadMultipart(url, params)
        """
        file=self.FILE_PATH + self.FILE_NAME
        fileUri=self.uri
        fileType=self.FILE_TYPE
        localeIdsToAuthorize=[self.MY_LOCALE]
        res, status = self.api.uploadSourceFile(file=file, fileUri=fileUri, fileType=fileType, localeIdsToAuthorize=localeIdsToAuthorize)
        
        
        assert_equal(res.data.wordCount, 6)
        assert_equal(res.data.stringCount, 6)
        
        print("uploadSourceFile", "OK")


    def checkDownloadSourceFile(self):
        """
            get
            /files-api/v2/projects/{projectId}/file
            for details check: https://api-reference.smartling.com/#operation/downloadSourceFile
            curl -H "Authorization: Bearer $smartlingToken" -G --data-urlencode "fileUri=$smartlingFileUri" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file"

            ------------------------------------------------------------------------------------------------------------------------
            def commandUpload(self, filePath, fileType, directives={}, **kw):
                ''' https://developer.smartling.com/v1.0/reference#upload '''
                params = {
                        Params.FILE_URI: filePath,
                        Params.FILE_TYPE: fileType,
                        Params.FILE_PATH: filePath
                    }
        
                for k,v in list(kw.items()):
                    params[k] = v
        
                self.addLibIdDirective(params)
                self.processDirectives(params, directives)
        
                url = self.urlHelper.getUrl(self.urlHelper.UPLOAD)
                return self.uploadMultipart(url, params)
        """
        fileUri=self.uri
        res, status = self.api.downloadSourceFile(fileUri=fileUri)
        
        
        orig = open(self.FILE_PATH + self.FILE_NAME, "rb").read()
        assert_equal(res, orig)
        
        print("downloadSourceFile", "OK")


    def checkGetFileTranslationStatusAllLocales(self):
        """
            get
            /files-api/v2/projects/{projectId}/file/status
            for details check: https://api-reference.smartling.com/#operation/getFileTranslationStatusAllLocales

            ------------------------------------------------------------------------------------------------------------------------
            def commandStatus(self, fileUri):
                ''' https://developer.smartling.com/v1.0/reference#get_projects-projectid-file-status '''
                kw = {}
                kw[Params.FILE_URI] = fileUri
                url = self.urlHelper.getUrl(self.urlHelper.STATUS_ALL)
                return self.command(ReqMethod.GET, url, kw)
        """
        fileUri=self.uri
        res, status = self.api.getFileTranslationStatusAllLocales(fileUri=fileUri)
        
        
        assert_equal(res.data.fileUri, self.uri)
        assert_equal(True, len(res.data.items) > 0)
        
        print("getFileTranslationStatusAllLocales", "OK")


    def checkGetFileTranslationStatusSingleLocale(self):
        """
            get
            /files-api/v2/projects/{projectId}/locales/{localeId}/file/status
            for details check: https://api-reference.smartling.com/#operation/getFileTranslationStatusSingleLocale

            ------------------------------------------------------------------------------------------------------------------------
            def commandStatusLocale(self, fileUri, localeId):
                ''' https://developer.smartling.com/v1.0/reference#get_projects-projectid-locales-localeid-file-status '''
                kw = {}
                kw[Params.FILE_URI] = fileUri
                url = self.urlHelper.getUrl(self.urlHelper.STATUS_LOCALE, localeId = localeId)
                return self.command(ReqMethod.GET, url, kw)
        """
        localeId=self.MY_LOCALE
        fileUri=self.uri
        res, status = self.api.getFileTranslationStatusSingleLocale(localeId=localeId, fileUri=fileUri)
        
        
        assert_equal(res.data.fileUri, self.uri)
        assert_equal(res.data.fileType, self.FILE_TYPE)
        
        print("getFileTranslationStatusSingleLocale", "OK")


    def checkDownloadTranslatedFileSingleLocale(self):
        """
            get
            /files-api/v2/projects/{projectId}/locales/{localeId}/file
            for details check: https://api-reference.smartling.com/#operation/downloadTranslatedFileSingleLocale
            curl -H "Authorization: Bearer $smartlingToken" -o $smartlingLocaleId$smartlingFileUri -G --data-urlencode "fileUri=$smartlingFileUri" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file"

            ------------------------------------------------------------------------------------------------------------------------
            def commandGet(self, fileUri, locale, directives={}, **kw):
                ''' https://developer.smartling.com/v1.0/reference#get_projects-projectid-locales-localeid-file '''
                kw[Params.FILE_URI] = fileUri
        
                self.checkRetrievalType(kw)
                self.processDirectives(kw, directives)
                url = self.urlHelper.getUrl(self.urlHelper.GET, localeId=locale)
        
                resp, code, headers = self.getResponseAndStatus(ReqMethod.GET, url, kw)
                return resp, code
        """
        localeId=self.MY_LOCALE
        fileUri=self.uri
        res, status = self.api.downloadTranslatedFileSingleLocale(localeId=localeId, fileUri=fileUri)
        
        
        resp_lines_count = len(res.decode('utf-8').split('\n'))
        file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME, "rb").read().decode('utf-8').split('\n') )
        assert_equal(resp_lines_count, file_lines_count)
        
        print("downloadTranslatedFileSingleLocale", "OK")


    def checkDownloadTranslatedFilesAllLocales(self):
        """
            get
            /files-api/v2/projects/{projectId}/locales/all/file/zip
            for details check: https://api-reference.smartling.com/#operation/downloadTranslatedFilesAllLocales
            curl -X GET -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/files-api/v2/projects/{projectId}/locales/all/file/zip?fileUri=yourfile.json&retrievalType=published'

            ------------------------------------------------------------------------------------------------------------------------
            def commandGetAllLocalesZip(self, fileUri, directives={}, **kw):
                 ''' http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/All-Locales '''
                 kw[Params.FILE_URI] = fileUri
        
                 self.checkRetrievalType(kw)
                 self.processDirectives(kw, directives)
        
                 url = self.urlHelper.getUrl(self.urlHelper.GET_ALL_LOCALES_ZIP)
        
                 resp, code, headers = self.getResponseAndStatus(ReqMethod.GET, url, kw)
                 return resp, code
        """
        fileUri=self.uri
        res, status = self.api.downloadTranslatedFilesAllLocales(fileUri=fileUri)
        
        
        zfile = self.getZipFile(res)
        names = zfile.namelist()
        assert_equal(True, self.MY_LOCALE+'/'+self.uri in names)
        
        print("downloadTranslatedFilesAllLocales", "OK")


    def checkDownloadMultipleTranslatedFiles(self):
        """
            get
            /files-api/v2/projects/{projectId}/files/zip
            for details check: https://api-reference.smartling.com/#operation/downloadMultipleTranslatedFiles

            ------------------------------------------------------------------------------------------------------------------------
            def commandGetMultipleLocalesAsZip(self, fileUri, localeIds, directives={}, **kw):
                ''' https://developer.smartling.com/v1.0/reference#get_projects-projectid-files-zip '''
                kw[Params.FILE_URIS] = fileUri
                kw[Params.LOCALE_IDS] = localeIds
        
                self.checkRetrievalType(kw)
                self.processDirectives(kw, directives)
        
                resp, code, headers = self.getResponseAndStatus(ReqMethod.GET, self.urlHelper.getUrl(self.urlHelper.GET_MULTIPLE_LOCALES), kw)
                return resp, code
        """
        fileUris=[self.uri,self.uri16]
        localeIds=[self.MY_LOCALE, 'zh-TW']
        res, status = self.api.downloadMultipleTranslatedFiles(fileUris=fileUris, localeIds=localeIds)
        
        
        zfile = self.getZipFile(res)
        names = zfile.namelist()
        assert_equal(True, self.MY_LOCALE+'/'+self.uri in names)
        assert_equal(True, self.MY_LOCALE+'/'+self.uri16 in names)
        assert_equal(True, 'zh-TW'+'/'+self.uri in names)
        assert_equal(True, 'zh-TW'+'/'+self.uri16 in names)
        
        print("downloadMultipleTranslatedFiles", "OK")


    def checkGetRecentlyUploadedSourceFilesList(self):
        """
            get
            /files-api/v2/projects/{projectId}/files/list
            for details check: https://api-reference.smartling.com/#operation/getRecentlyUploadedSourceFilesList
            curl -H "Authorization: Bearer $smartlingToken" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/files/list?fileTypes[]=json&uriMask=strings"

            ------------------------------------------------------------------------------------------------------------------------
            def commandList(self, **kw):
                ''' https://developer.smartling.com/v1.0/reference#list '''
                url = self.urlHelper.getUrl(self.urlHelper.LIST_FILES)
                self.validateFileTypes(kw)
        
                return self.command(ReqMethod.GET, url, kw)
        """
        fileTypes=[FileTypes.android, FileTypes.javaProperties]
        res, status = self.api.getRecentlyUploadedSourceFilesList(fileTypes=fileTypes)
        
        
        uris = [x['fileUri'] for x in res.data.items]
        assert_equal(True, self.uri in uris)
        assert_equal(True, self.uri16 in uris)
        
        print("getRecentlyUploadedSourceFilesList", "OK")


    def checkGetFileTypesList(self):
        """
            get
            /files-api/v2/projects/{projectId}/file-types
            for details check: https://api-reference.smartling.com/#operation/getFileTypesList
            curl -H "Authorization: Bearer $smartlingToken" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file-types"

            ------------------------------------------------------------------------------------------------------------------------
            def commandListFileTypes(self, **kw):
                ''' https://developer.smartling.com/v1.0/reference#get_projects-projectid-file-types '''
                return self.command(ReqMethod.GET, self.urlHelper.getUrl(self.urlHelper.LIST_FILE_TYPES), kw)
        """
        res, status = self.api.getFileTypesList()
        
        
        assert_equal(True, "javaProperties" in res.data.items)
        
        print("getFileTypesList", "OK")


    def checkRenameUploadedSourceFile(self):
        """
            post
            /files-api/v2/projects/{projectId}/file/rename
            for details check: https://api-reference.smartling.com/#operation/renameUploadedSourceFile
            curl -X POST -H "Authorization: Bearer $smartlingToken" -F "fileUri=filename.properties" -F "newFileUri=filename2.properties" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file/rename'

            ------------------------------------------------------------------------------------------------------------------------
            def commandRename(self, fileUri, newFileUrl):
                ''' https://developer.smartling.com/v1.0/reference#rename '''
                kw = {}
                kw[Params.FILE_URI] = fileUri
                kw[Params.FILE_URI_NEW] = newFileUrl
                url = self.urlHelper.getUrl(self.urlHelper.RENAME)
                return self.command(ReqMethod.POST, url, kw)
        """
        fileUri=self.uri
        newFileUri=self.uri_to_rename
        res, status = self.api.renameUploadedSourceFile(fileUri=fileUri, newFileUri=newFileUri)
        
        
        res, status = self.api.renameUploadedSourceFile(self.uri_to_rename, self.uri) #rename it back so in the end it could be removed
        
        print("renameUploadedSourceFile", "OK")


    def checkGetTranslatedFileLastModifiedDateSingleLocale(self):
        """
            get
            /files-api/v2/projects/{projectId}/locales/{localeId}/file/last-modified
            for details check: https://api-reference.smartling.com/#operation/getTranslatedFileLastModifiedDateSingleLocale
            curl -X GET -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file/last-modified?fileUri=filename.properties'

            ------------------------------------------------------------------------------------------------------------------------
            def commandLastModified(self, fileUri, localeId, **kw):
                ''' https://developer.smartling.com/v1.0/reference#last-modified '''
                kw[Params.FILE_URI] = fileUri
                url = self.urlHelper.getUrl(self.urlHelper.LAST_MODIFIED, localeId = localeId)
                return self.command(ReqMethod.GET, url, kw)
        """
        localeId=self.MY_LOCALE
        fileUri=self.uri
        res, status = self.api.getTranslatedFileLastModifiedDateSingleLocale(localeId=localeId, fileUri=fileUri)
        
        
        lm_date = res.data.lastModified[:10]
        assert_equal(lm_date,  date.today().isoformat())
        
        print("getTranslatedFileLastModifiedDateSingleLocale", "OK")


    def checkGetTranslatedFileLastModifiedDateAllLocales(self):
        """
            get
            /files-api/v2/projects/{projectId}/file/last-modified
            for details check: https://api-reference.smartling.com/#operation/getTranslatedFileLastModifiedDateAllLocales
            curl -X GET -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file/last-modified?fileUri=filename.properties'

            ------------------------------------------------------------------------------------------------------------------------
            def commandLastModifiedAll(self, fileUri, **kw):
                ''' https://developer.smartling.com/v1.0/reference#get_projects-projectid-file-last-modified '''
                kw[Params.FILE_URI] = fileUri
                url = self.urlHelper.getUrl(self.urlHelper.LAST_MODIFIED_ALL)
                return self.command(ReqMethod.GET, url, kw)
        """
        fileUri=self.uri
        res, status = self.api.getTranslatedFileLastModifiedDateAllLocales(fileUri=fileUri)
        
        
        assert_equal(True, len(res.data.items) > 0)
        for l in res.data.items:
            if l['localeId'] == self.MY_LOCALE:
                lm_date = l['lastModified'][:10]
                assert_equal(lm_date,  date.today().isoformat())
        
        print("getTranslatedFileLastModifiedDateAllLocales", "OK")


    def checkImportFileTranslations(self):
        """
            post
            /files-api/v2/projects/{projectId}/locales/{localeId}/file/import
            for details check: https://api-reference.smartling.com/#operation/importFileTranslations
            curl -H "Authorization: Bearer $smartlingToken" -F "file=@filename.properties" -F "fileUri=filename.properties" -F "fileType=javaProperties" -F "translationState=PUBLISHED" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file/import'

            ------------------------------------------------------------------------------------------------------------------------
            def commandImport(self, fileUriOriginal, filePathTranslated, fileType, localeId, directives={}, **kw):
                self.validateFileTypes({"fileTypes":fileType})
                params = {}
                params[Params.FILE_URI]  = fileUriOriginal
                params[Params.FILE_TYPE] = fileType
                params[Params.FILE_PATH] = filePathTranslated
                params["file"] = filePathTranslated + ";type=text/plain"
        
                for k,v in list(kw.items()):
                    params[k] = v
        
                self.processDirectives(params, directives)
        
                url = self.urlHelper.getUrl(self.urlHelper.IMPORT, localeId = localeId)
                return self.uploadMultipart(url, params)
        """
        res, status = self.api.uploadSourceFile(self.FILE_PATH + self.FILE_NAME_IMPORT_ORIG, fileType = self.FILE_TYPE_IMPORT , fileUri=self.uri_import)
        localeId=self.MY_LOCALE
        file=self.FILE_PATH + self.FILE_NAME_IMPORT_TRANSLATED
        fileUri=self.uri_import
        fileType=self.FILE_TYPE_IMPORT
        translationState='PUBLISHED'
        res, status = self.api.importFileTranslations(localeId=localeId, file=file, fileUri=fileUri, fileType=fileType, translationState=translationState)
        
        
        
        assert_equal(res.data.wordCount, 2)
        assert_equal(res.data.stringCount, 2)
        assert_equal(res.data.translationImportErrors, [])
        
        res, status = self.api.deleteUploadedSourceFile(self.uri_import)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        
        print("importFileTranslations", "OK")


    def checkExportFileTranslations(self):
        """
            post
            /files-api/v2/projects/{projectId}/locales/{localeId}/file/get-translations
            for details check: https://api-reference.smartling.com/#operation/exportFileTranslations
            curl -H "Authorization: Bearer $smartlingToken" -F "file=@filename.properties" -F 'fileUri=filename.properties' 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file/get-translations'

            ------------------------------------------------------------------------------------------------------------------------
            def commandGetTranslations(self, fileUri, filePath, localeId, directives={}, **kw):
                '''  https://developer.smartling.com/v1.0/reference#post_projects-projectid-locales-localeid-file-import '''
                kw[Params.FILE_URI]  = fileUri
                kw[Params.FILE_PATH] = filePath
                kw["file"] = filePath + ";type=text/plain"
        
                self.processDirectives(kw, directives)
        
                url = self.urlHelper.getUrl(self.urlHelper.GET_TRANSLATIONS, localeId = localeId)
                return self.uploadMultipart(url, kw, response_as_string=True)
        """
        localeId=self.MY_LOCALE
        file=self.FILE_PATH+self.FILE_NAME
        fileUri=self.uri
        res, status = self.api.exportFileTranslations(localeId=localeId, file=file, fileUri=fileUri)
        
        
        resp_lines_count = len(res.split(newline))
        file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME, "rb").readlines() )
        assert_equal(resp_lines_count, file_lines_count)
        
        print("exportFileTranslations", "OK")


    def checkGetRecentlyPublishedFilesList(self):
        """
            get
            /published-files-api/v2/projects/{projectId}/files/list/recently-published
            for details check: https://api-reference.smartling.com/#operation/getRecentlyPublishedFilesList
            curl -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/published-files-api/v2/projects/$smartlingProjectId/files/list/recently-published?publishedAfter=2019-11-21T11:51:17Z&fileUris[]=files/example1.json&localeIds[]=fr-CA&limit=10&offset=100'

            ------------------------------------------------------------------------------------------------------------------------
        """
        publishedAfter=datetime.datetime.fromtimestamp(time.time()-10*24*2600).strftime("%Y-%m-%d")
        localeIds=[self.MY_LOCALE]
        res, status = self.api.getRecentlyPublishedFilesList(publishedAfter=publishedAfter, localeIds=localeIds)
        
        
        assert_equal(True, len(res.data.items) > 0)
        
        print("getRecentlyPublishedFilesList", "OK")


    def checkDeleteUploadedSourceFile(self):
        """
            post
            /files-api/v2/projects/{projectId}/file/delete
            for details check: https://api-reference.smartling.com/#operation/deleteUploadedSourceFile
            curl -X POST -H "Authorization: Bearer $smartlingToken" -F "fileUri=filename.properties" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file/delete'

            ------------------------------------------------------------------------------------------------------------------------
            def commandDelete(self, fileUri, **kw):
                ''' https://developer.smartling.com/v1.0/reference#delete '''
                kw[Params.FILE_URI] = fileUri
                uri = self.urlHelper.getUrl(self.urlHelper.DELETE)
        
                return self.command(ReqMethod.POST, uri, kw)
        """
        fileUri=self.uri
        res, status = self.api.deleteUploadedSourceFile(fileUri=fileUri)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print("deleteUploadedSourceFile", "OK")



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
