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

from .HttpClient import HttpClient
from .MultipartPostHandler import MultipartPostHandler
from .Constants import Params, ReqMethod
from .ApiResponse import ApiResponse
from .AuthClient import AuthClient
from .Constants import FileTypes

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

class ApiV2:
    """ basic class implementing low-level api calls """
    host = 'api.smartling.com'
    response_as_string = False

    def __init__(self, userIdentifier, userSecret, proxySettings=None):
        self.userIdentifier = userIdentifier
        self.userSecret = userSecret
        self.proxySettings = proxySettings
        self.httpClient = HttpClient(self.host, proxySettings)
        self.authClient = AuthClient(userIdentifier, userSecret, proxySettings)

    def uploadMultipart(self, uri, params, response_as_string=False):
        if Params.FILE_PATH in params:
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
            raise Exception("Error getting token, check you credentials")

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
                raise Exception(unsupported)

    def checkRetrievalType(self, kw):
        if Params.RETRIEVAL_TYPE in kw and not kw[Params.RETRIEVAL_TYPE] in Params.allowedRetrievalTypes:
            Exception( "Not allowed value `%s` for parameter:%s try one of %s" % (kw[Params.RETRIEVAL_TYPE],
                                                                             Params.RETRIEVAL_TYPE,
                                                                             Params.allowedRetrievalTypes) )

    def processDirectives(self, params, directives):
        for name, value in list(directives.items()):
           params["smartling." + name] = value
