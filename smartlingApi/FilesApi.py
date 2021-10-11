
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


from smartlingApiSdk.ApiV2 import ApiV2

class FilesApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def uploadSourceFile(self, file, fileUri, fileType, authorize=False, localeIdsToAuthorize=[], callbackUrl='', directives={}, **kwargs):
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
        kw = {
            'file':self.processFile(file),
            'fileUri':fileUri,
            'fileType':fileType,
            'authorize':authorize,
            'localeIdsToAuthorize':localeIdsToAuthorize,
            'callbackUrl':callbackUrl,
        }
        self.addLibIdDirective(kw)
        self.processDirectives(kw, directives)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file')
        return self.uploadMultipart(url, kw)


    def downloadSourceFile(self, fileUri, **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/file
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G --data-urlencode "fileUri=$smartlingFileUri" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/downloadSourceFile
        """
        kw = {
            'fileUri':fileUri,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getFileTranslationStatusAllLocales(self, fileUri, **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/file/status
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getFileTranslationStatusAllLocales
        """
        kw = {
            'fileUri':fileUri,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file/status', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getFileTranslationStatusSingleLocale(self, localeId, fileUri, **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file/status
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getFileTranslationStatusSingleLocale
        """
        kw = {
            'fileUri':fileUri,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file/status', localeId=localeId, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def downloadTranslatedFileSingleLocale(self, localeId, fileUri, retrievalType='', includeOriginalStrings='', **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -o $smartlingLocaleId$smartlingFileUri -G --data-urlencode "fileUri=$smartlingFileUri" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/downloadTranslatedFileSingleLocale
        """
        kw = {
            'fileUri':fileUri,
            'retrievalType':retrievalType,
            'includeOriginalStrings':includeOriginalStrings,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file', localeId=localeId, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def downloadTranslatedFilesAllLocales(self, fileUri, retrievalType='', includeOriginalStrings='', zipFileName='', **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/locales/all/file/zip
            as curl :  curl -X GET -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/files-api/v2/projects/{projectId}/locales/all/file/zip?fileUri=yourfile.json&retrievalType=published'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/downloadTranslatedFilesAllLocales
        """
        kw = {
            'fileUri':fileUri,
            'retrievalType':retrievalType,
            'includeOriginalStrings':includeOriginalStrings,
            'zipFileName':zipFileName,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/all/file/zip', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def downloadMultipleTranslatedFiles(self, fileUris, localeIds, retrievalType='', includeOriginalStrings='', fileNameMode='', localeMode='', zipFileName='', **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/files/zip
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/downloadMultipleTranslatedFiles
        """
        kw = {
            'fileUris':fileUris,
            'localeIds':localeIds,
            'retrievalType':retrievalType,
            'includeOriginalStrings':includeOriginalStrings,
            'fileNameMode':fileNameMode,
            'localeMode':localeMode,
            'zipFileName':zipFileName,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/files/zip', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getRecentlyUploadedSourceFilesList(self, uriMask='', fileTypes=[], lastUploadedAfter='', lastUploadedBefore='', orderBy='', limit=100, offset=0, **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/files/list
            as curl :  curl -H "Authorization: Bearer $smartlingToken" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/files/list?fileTypes[]=json&uriMask=strings"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getRecentlyUploadedSourceFilesList
        """
        kw = {
            'uriMask':uriMask,
            'fileTypes':fileTypes,
            'lastUploadedAfter':lastUploadedAfter,
            'lastUploadedBefore':lastUploadedBefore,
            'orderBy':orderBy,
            'limit':limit,
            'offset':offset,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/files/list', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getFileTypesList(self, **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/file-types
            as curl :  curl -H "Authorization: Bearer $smartlingToken" "https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file-types"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getFileTypesList
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file-types', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def renameUploadedSourceFile(self, fileUri, newFileUri, **kwargs):
        """
            method  :  POST
            api url :  /files-api/v2/projects/{projectId}/file/rename
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -F "fileUri=filename.properties" -F "newFileUri=filename2.properties" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file/rename'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/renameUploadedSourceFile
        """
        kw = {
            'fileUri':fileUri,
            'newFileUri':newFileUri,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file/rename', **kwargs)
        response, status = self.command('POST', url, kw)
        return response, status


    def deleteUploadedSourceFile(self, fileUri, **kwargs):
        """
            method  :  POST
            api url :  /files-api/v2/projects/{projectId}/file/delete
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -F "fileUri=filename.properties" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file/delete'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/deleteUploadedSourceFile
        """
        kw = {
            'fileUri':fileUri,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file/delete', **kwargs)
        response, status = self.command('POST', url, kw)
        return response, status


    def getTranslatedFileLastModifiedDateSingleLocale(self, localeId, fileUri, lastModifiedAfter='', **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file/last-modified
            as curl :  curl -X GET -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file/last-modified?fileUri=filename.properties'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getTranslatedFileLastModifiedDateSingleLocale
        """
        kw = {
            'fileUri':fileUri,
            'lastModifiedAfter':lastModifiedAfter,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file/last-modified', localeId=localeId, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getTranslatedFileLastModifiedDateAllLocales(self, fileUri, lastModifiedAfter='', **kwargs):
        """
            method  :  GET
            api url :  /files-api/v2/projects/{projectId}/file/last-modified
            as curl :  curl -X GET -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/file/last-modified?fileUri=filename.properties'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getTranslatedFileLastModifiedDateAllLocales
        """
        kw = {
            'fileUri':fileUri,
            'lastModifiedAfter':lastModifiedAfter,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file/last-modified', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def importFileTranslations(self, localeId, file, fileUri, fileType, translationState, overwrite='', **kwargs):
        """
            method  :  POST
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file/import
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -F "file=@filename.properties" -F "fileUri=filename.properties" -F "fileType=javaProperties" -F "translationState=PUBLISHED" 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file/import'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/importFileTranslations
        """
        kw = {
            'file':self.processFile(file),
            'fileUri':fileUri,
            'fileType':fileType,
            'translationState':translationState,
            'overwrite':overwrite,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file/import', localeId=localeId)
        return self.uploadMultipart(url, kw)


    def exportFileTranslations(self, localeId, file, fileUri, retrievalType='', includeOriginalStrings='', **kwargs):
        """
            method  :  POST
            api url :  /files-api/v2/projects/{projectId}/locales/{localeId}/file/get-translations
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -F "file=@filename.properties" -F 'fileUri=filename.properties' 'https://api.smartling.com/files-api/v2/projects/$smartlingProjectId/locales/$smartlingLocaleId/file/get-translations'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/exportFileTranslations
        """
        kw = {
            'file':self.processFile(file),
            'fileUri':fileUri,
            'retrievalType':retrievalType,
            'includeOriginalStrings':includeOriginalStrings,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file/get-translations', localeId=localeId)
        return self.uploadMultipart(url, kw)


    def getRecentlyPublishedFilesList(self, publishedAfter, fileUris=[], localeIds=[], offset=0, limit=0, **kwargs):
        """
            method  :  GET
            api url :  /published-files-api/v2/projects/{projectId}/files/list/recently-published
            as curl :  curl -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/published-files-api/v2/projects/$smartlingProjectId/files/list/recently-published?publishedAfter=2019-11-21T11:51:17Z&fileUris[]=files/example1.json&localeIds[]=fr-CA&limit=10&offset=100'
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getRecentlyPublishedFilesList
        """
        kw = {
            'publishedAfter':publishedAfter,
            'fileUris':fileUris,
            'localeIds':localeIds,
            'offset':offset,
            'limit':limit,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/published-files-api/v2/projects/{projectId}/files/list/recently-published', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status

