from .UrlV2Helper import UrlV2Helper
from .ApiV2 import ApiV2

class FilesApiAuto(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None):
        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings)
        self.urlHelper = UrlV2Helper(projectId)

    def uploadSourceFile(self, file, fileUri, fileType, authorize=False, localeIdsToAuthorize=[], callbackUrl='', directives={}):
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




    def downloadSourceFile(self, fileUri):
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
        kw = {
            'fileUri':fileUri,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file')
        return self.command('GET', url, kw)




    def getFileTranslationStatusAllLocales(self, fileUri):
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
        kw = {
            'fileUri':fileUri,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file/status')
        return self.command('GET', url, kw)




    def getFileTranslationStatusSingleLocale(self, localeId, fileUri):
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
        kw = {
            'fileUri':fileUri,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file/status', localeId=localeId)
        return self.command('GET', url, kw)




    def downloadTranslatedFileSingleLocale(self, localeId, fileUri, retrievalType='', includeOriginalStrings=''):
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
        kw = {
            'fileUri':fileUri,
            'retrievalType':retrievalType,
            'includeOriginalStrings':includeOriginalStrings,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file', localeId=localeId)
        return self.command('GET', url, kw)




    def downloadTranslatedFilesAllLocales(self, fileUri, retrievalType='', includeOriginalStrings='', zipFileName=''):
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
        kw = {
            'fileUri':fileUri,
            'retrievalType':retrievalType,
            'includeOriginalStrings':includeOriginalStrings,
            'zipFileName':zipFileName,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/all/file/zip')
        return self.command('GET', url, kw)




    def downloadMultipleTranslatedFiles(self, fileUris, localeIds, retrievalType='', includeOriginalStrings='', fileNameMode='', localeMode='', zipFileName=''):
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
        kw = {
            'fileUris':fileUris,
            'localeIds':localeIds,
            'retrievalType':retrievalType,
            'includeOriginalStrings':includeOriginalStrings,
            'fileNameMode':fileNameMode,
            'localeMode':localeMode,
            'zipFileName':zipFileName,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/files/zip')
        return self.command('GET', url, kw)




    def getRecentlyUploadedSourceFilesList(self, uriMask='', fileTypes=[], lastUploadedAfter='', lastUploadedBefore='', orderBy='', limit=0, offset=0):
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
        kw = {
            'uriMask':uriMask,
            'fileTypes':fileTypes,
            'lastUploadedAfter':lastUploadedAfter,
            'lastUploadedBefore':lastUploadedBefore,
            'orderBy':orderBy,
            'limit':limit,
            'offset':offset,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/files/list')
        return self.command('GET', url, kw)




    def getFileTypesList(self):
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
        kw = {
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file-types')
        return self.command('GET', url, kw)




    def renameUploadedSourceFile(self, fileUri, newFileUri):
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
        kw = {
            'fileUri':fileUri,
            'newFileUri':newFileUri,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file/rename')
        return self.command('POST', url, kw)




    def deleteUploadedSourceFile(self, fileUri):
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
        kw = {
            'fileUri':fileUri,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file/delete')
        return self.command('POST', url, kw)




    def getTranslatedFileLastModifiedDateSingleLocale(self, localeId, fileUri, lastModifiedAfter=''):
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
        kw = {
            'fileUri':fileUri,
            'lastModifiedAfter':lastModifiedAfter,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file/last-modified', localeId=localeId)
        return self.command('GET', url, kw)




    def getTranslatedFileLastModifiedDateAllLocales(self, fileUri, lastModifiedAfter=''):
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
        kw = {
            'fileUri':fileUri,
            'lastModifiedAfter':lastModifiedAfter,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/file/last-modified')
        return self.command('GET', url, kw)




    def importFileTranslations(self, localeId, file, fileUri, fileType, translationState, overwrite=''):
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
        kw = {
            'file':self.processFile(file),
            'fileUri':fileUri,
            'fileType':fileType,
            'translationState':translationState,
            'overwrite':overwrite,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file/import', localeId=localeId)
        return self.uploadMultipart(url, kw)




    def exportFileTranslations(self, localeId, file, fileUri, retrievalType='', includeOriginalStrings=''):
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
        kw = {
            'file':self.processFile(file),
            'fileUri':fileUri,
            'retrievalType':retrievalType,
            'includeOriginalStrings':includeOriginalStrings,
        }
        url = self.urlHelper.getUrl('/files-api/v2/projects/{projectId}/locales/{localeId}/file/get-translations', localeId=localeId)
        return self.uploadMultipart(url, kw)




    def getRecentlyPublishedFilesList(self, publishedAfter, fileUris=[], localeIds=[], offset=0, limit=0):
        """
            get
            /published-files-api/v2/projects/{projectId}/files/list/recently-published
            for details check: https://api-reference.smartling.com/#operation/getRecentlyPublishedFilesList
            curl -H "Authorization: Bearer $smartlingToken" 'https://api.smartling.com/published-files-api/v2/projects/$smartlingProjectId/files/list/recently-published?publishedAfter=2019-11-21T11:51:17Z&fileUris[]=files/example1.json&localeIds[]=fr-CA&limit=10&offset=100'

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'publishedAfter':publishedAfter,
            'fileUris':fileUris,
            'localeIds':localeIds,
            'offset':offset,
            'limit':limit,
        }
        url = self.urlHelper.getUrl('/published-files-api/v2/projects/{projectId}/files/list/recently-published')
        return self.command('GET', url, kw)



