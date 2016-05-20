#!/usr/bin/python
# -*- coding: utf-8 -*-


''' Copyright 2012 Smartling, Inc.
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

#FileApi class implementation

from HttpClient import HttpClient
from MultipartPostHandler import MultipartPostHandler
from Constants import Uri, Params, ReqMethod
from ApiResponse import ApiResponse
from AuthClient import AuthClient
from UrlV2Helper import UrlV2Helper
from Constants import FileTypes

"""
Upload File - /files-api/v2/projects/{projectId}/file (POST)
Download Original File - /files-api/v2/projects/{projectId}/file (GET)
Download Translated File - Single Locale - /files-api/v2/projects/{projectId}/locales/{localeId}/file (GET)
Download Translated Files - Multiple Locales as .ZIP - /files-api/v2/projects/{projectId}/files/zip (GET)
Download Translated File - All Locales as .ZIP - /files-api/v2/projects/{projectId}/locales/all/file/zip (GET)
Download Translated File - All Locales in one File - CSV - /files-api/v2/projects/{projectId}/locales/all/file (GET)
List Files - /files-api/v2/projects/{projectId}/files/list (GET)
List File Types - /files-api/v2/projects/{projectId}/file-types (GET)
Status - All Locales - /files-api/v2/projects/{projectId}/file/status (GET)
Status - Single Locale / Extended Response - /files-api/v2/projects/{projectId}/locales/{localeId}/file/status (GET)
Rename - /files-api/v2/projects/{projectId}/file/rename (POST)
Delete - /files-api/v2/projects/{projectId}/file/delete (POST)
Last Modified (by locale) - /files-api/v2/projects/{projectId}/locales/{localeId}/file/last-modified (GET)
Last Modified (all locales) - /files-api/v2/projects/{projectId}/file/last-modified (GET)
Import Translations - /files-api/v2/projects/{projectId}/locales/{localeId}/file/import (POST or PUT)
List Authorized Locales - /files-api/v2/projects/{projectId}/file/authorized-locales (GET)
Authorize - /files-api/v2/projects/{projectId}/file/authorized-locales (PUT / POST)
Unauthorize - /files-api/v2/projects/{projectId}/file/authorized-locales (DELETE)
Get Translations - /files-api/v2/projects/{projectId}/locales/{localeId}/file/get-translations (POST)
"""

class FileApiV2:
    """ basic class implementing low-level api calls """
    host = 'api.smartling.com'
    response_as_string = False

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None):
        self.userIdentifier = userIdentifier
        self.userSecret = userSecret
        self.projectId = projectId
        self.proxySettings = proxySettings
        self.httpClient = HttpClient(self.host, proxySettings)
        self.authClient = AuthClient(userIdentifier, userSecret, proxySettings)
        self.urlHelper = UrlV2Helper(self.projectId)

    def uploadMultipart(self, uri, params, response_as_string=False):
        if params.has_key(Params.FILE_PATH):
            params[Params.FILE] = open(params[Params.FILE_PATH], 'rb')
            del params[Params.FILE_PATH]  # no need in extra field in POST

        authHeader = self.getAuthHeader()  
        response_data, status_code = self.getHttpResponseAndStatus(ReqMethod.POST ,uri, params, MultipartPostHandler, extraHeaders = authHeader)
        response_data = response_data.strip()
        if self.response_as_string or response_as_string:
            return response_data, status_code
        return ApiResponse(response_data, status_code), status_code
  
    def getHttpResponseAndStatus(self, method, uri, params, handler=None, extraHeaders = None):
        return self.httpClient.getHttpResponseAndStatus(method, uri, params, handler, extraHeaders = extraHeaders)
  
    def getAuthHeader(self):
        token = self.authClient.getToken()
        if token is None:
            raise "Error getting token, check you credentials"
            
        return {"Authorization" : "Bearer "+ token} 
   
    def command_raw(self, method, uri, params):
        authHeader = self.getAuthHeader()
        return self.getHttpResponseAndStatus(method, uri, params, extraHeaders = authHeader)

    def command(self, method, uri, params):
        data, code = self.command_raw(method, uri, params)
        if self.response_as_string:
            return data, code
        return  ApiResponse(data, code), code

    def validateFileTypes(self, kw):
        fileTypes = kw.get("fileTypes",[])
        if type(fileTypes) != type([]) and type(fileTypes) != type(()):
            fileTypes = [fileTypes]
        for t in fileTypes: 
            if not getattr(FileTypes, t, None):
                unsupported = "\nUnsupported file type:%s\n" % t
                raise unsupported

    def checkRetrievalType(self, kw):
        if Params.RETRIEVAL_TYPE in kw and not kw[Params.RETRIEVAL_TYPE] in Params.allowedRetrievalTypes:
            raise "Not allowed value `%s` for parameter:%s try one of %s" % (kw[Params.RETRIEVAL_TYPE],
                                                                             Params.RETRIEVAL_TYPE,
                                                                             Params.allowedRetrievalTypes)

    def processDirectives(self, params, directives):
        for name, value in directives.items():
           params["smartling." + name] = value

#-----------------------------------------------------------------------------------

    def commandGet(self, fileUri, locale, directives={}, **kw):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/Single-Locale/ """
        kw[Params.FILE_URI] = fileUri
 
        self.checkRetrievalType(kw)
        self.processDirectives(kw, directives)
        url = self.urlHelper.getUrl(self.urlHelper.GET, localeId=locale)
        return self.command_raw(ReqMethod.GET, url, kw)

    def commandGetMultipleLocalesAsZip(self, fileUri, localeIds, directives={}, **kw):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/Multiple-Locales/ """
        kw[Params.FILE_URIS] = fileUri
        kw[Params.LOCALE_IDS] = localeIds
 
        self.checkRetrievalType(kw)
        self.processDirectives(kw, directives)
        
        return self.command_raw(ReqMethod.GET, self.urlHelper.getUrl(self.urlHelper.GET_MULTIPLE_LOCALES), kw)
 
    def commandGetAllLocalesZip(self, fileUri, directives={}, **kw):
         """ http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/All-Locales """
         kw[Params.FILE_URI] = fileUri
  
         self.checkRetrievalType(kw)
         self.processDirectives(kw, directives)

         url = self.urlHelper.getUrl(self.urlHelper.GET_ALL_LOCALES_ZIP)
         
         return self.command_raw(ReqMethod.GET, url, kw)
        

    def commandGetAllLocalesCsv(self, fileUri, directives={}, **kw):
         """  http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/All-Locales-CSV """
         kw[Params.FILE_URI] = fileUri
  
         self.checkRetrievalType(kw)
         self.processDirectives(kw, directives)

         url = self.urlHelper.getUrl(self.urlHelper.GET_ALL_LOCALES_CSV)
         return self.command_raw(ReqMethod.GET, url, kw)


    def commandGetOriginal(self, fileUri):
         """  http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/Original-File/ """
         kw = {}
         kw[Params.FILE_URI] = fileUri
  
         url = self.urlHelper.getUrl(self.urlHelper.GET_ORIGINAL)
         return self.command_raw(ReqMethod.GET, url, kw)            

    def commandList(self, **kw):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/List/ """
        url = self.urlHelper.getUrl(self.urlHelper.LIST_FILES)
        self.validateFileTypes(kw)
        
        return self.command(ReqMethod.GET, url, kw)
        
    def commandListFileTypes(self, **kw):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/List-File-Types/ """
        return self.command(ReqMethod.GET, self.urlHelper.getUrl(self.urlHelper.LIST_FILE_TYPES), kw)

    def commandUpload(self, filePath, fileType, directives={}, **kw):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Upload-File/ """
        params = {
                Params.FILE_URI: filePath,
                Params.FILE_TYPE: fileType,
                Params.FILE_PATH: filePath
            }

        for k,v in kw.items():
            params[k] = v

        self.processDirectives(params, directives)
        
        url = self.urlHelper.getUrl(self.urlHelper.UPLOAD)
        return self.uploadMultipart(url, params)
        
    def commandProjectDetails(self):    
        """ http://docs.smartling.com/pages/API/v2/Projects/Project-Details/ """
        kw = {}
        url = self.urlHelper.getUrl(self.urlHelper.PROJECT_DETAILS)
        return self.command(ReqMethod.GET, url, kw)
        
    def commandProjects(self, accountUid):    
        """ http://docs.smartling.com/pages/API/v2/Projects/List-Projects/ """
        kw = {}
        url = self.urlHelper.getUrl(self.urlHelper.PROJECTS, accountUid = accountUid)
        return self.command(ReqMethod.GET, url, kw)
        

    def commandDelete(self, fileUri, **kw):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Delete/ """
        kw[Params.FILE_URI] = fileUri
        uri = self.urlHelper.getUrl(self.urlHelper.DELETE)

        return self.command(ReqMethod.POST, uri, kw)
        
    def commandStatus(self, fileUri):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Status/All-Locales/ """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.STATUS_ALL)
        return self.command(ReqMethod.GET, url, kw)
        
    def commandStatusLocale(self, fileUri, localeId):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Status/Single-Locale/ """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.STATUS_LOCALE, localeId = localeId)
        return self.command(ReqMethod.GET, url, kw)     
            
    def commandRename(self, fileUri, newFileUrl):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Rename/ """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        kw[Params.FILE_URI_NEW] = newFileUrl
        url = self.urlHelper.getUrl(self.urlHelper.RENAME)
        return self.command(ReqMethod.POST, url, kw)

    def commandLastModified(self, fileUri, localeId, **kw):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Last-Modified/Single-Locale/ """
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.LAST_MODIFIED, localeId = localeId)
        return self.command(ReqMethod.GET, url, kw) 

    def commandLastModifiedAll(self, fileUri, **kw):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Last-Modified/All-Locales/ """
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.LAST_MODIFIED_ALL)
        return self.command(ReqMethod.GET, url, kw) 

    def commandImport(self, fileUriOriginal, filePathTranslated, fileType, localeId, directives={}, **kw):
        self.validateFileTypes({"fileTypes":fileType})
        params = {}
        params[Params.FILE_URI]  = fileUriOriginal
        params[Params.FILE_TYPE] = fileType
        params[Params.FILE_PATH] = filePathTranslated
        params["file"] = filePathTranslated + ";type=text/plain"

        for k,v in kw.items():
            params[k] = v
        
        self.processDirectives(params, directives)
        
        url = self.urlHelper.getUrl(self.urlHelper.IMPORT, localeId = localeId)
        return self.uploadMultipart(url, params)

    def commandListAuthorizedLocales(self, fileUri):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Authorize-Content/List-Authorized-Locales/ """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.LIST_AUTHORIZED_LOCALES)
        return self.command(ReqMethod.GET, url, kw) 

    def commandAuthorize(self, fileUri, localeIds):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Authorize-Content/Authorize/ """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE_IDS_BRACKET] = ",".join(localeIds)
        url = self.urlHelper.getUrl(self.urlHelper.AUTHORIZE)
        return self.command(ReqMethod.POST, url, kw)
        
    def commandUnauthorize(self, fileUri, localeIds):
        """  http://docs.smartling.com/pages/API/v2/FileAPI/Authorize-Content/Unauthorize/ """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE_IDS_BRACKET] = ",".join(localeIds)
        url = self.urlHelper.getUrl(self.urlHelper.UNAUTHORIZE)
        return self.command(ReqMethod.DELETE, url, kw)
        
    def commandGetTranslations(self, fileUri, filePath, localeId, directives={}, **kw):
        """  http://docs.smartling.com/pages/API/v2/FileAPI/Get-Translations/ """
        kw[Params.FILE_URI]  = fileUri
        kw[Params.FILE_PATH] = filePath
        kw["file"] = filePath + ";type=text/plain"
        
        self.processDirectives(kw, directives)

        url = self.urlHelper.getUrl(self.urlHelper.GET_TRANSLATIONS, localeId = localeId)
        return self.uploadMultipart(url, kw, response_as_string=True)       
       