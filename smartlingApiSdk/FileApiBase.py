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
from .Constants import Uri, Params, ReqMethod
from .ApiResponse import ApiResponse
from .Logger import Logger
import sys

class FileApiBase:
    """ basic class implementing low-level api calls """
    response_as_string = False

    def __init__(self, host, apiKey, projectId, proxySettings=None):
        self.host = host
        self.apiKey = apiKey
        self.projectId = projectId
        self.proxySettings = proxySettings
        self.httpClient = HttpClient(host, proxySettings)

        logger = Logger()
        sys.stdout = logger

    def addAuth(self, params):
        params[Params.API_KEY] = self.apiKey
        params[Params.PROJECT_ID] = self.projectId
        return {}

    def uploadMultipart(self, uri, params, response_as_string=False):
        authHeader = self.addAuth(params)

        if Params.FILE_PATH in params:
            params[Params.FILE] = open(params[Params.FILE_PATH], 'rb')
            del params[Params.FILE_PATH]  # no need in extra field in POST

        response_data, status_code = self.getHttpResponseAndStatus(ReqMethod.POST ,uri, params, MultipartPostHandler, extraHeaders = authHeader)
        response_data = response_data.strip()
        if self.response_as_string or response_as_string:
            return response_data, status_code
        return ApiResponse(response_data, status_code), status_code

    def getHttpResponseAndStatus(self, method, uri, params, handler=None, extraHeaders = None):
        return self.httpClient.getHttpResponseAndStatus(method, uri, params, handler, extraHeaders = extraHeaders)
  
    def getResponseAndStatus(self, method, uri, params):
        authHeader = self.addAuth(params)
        return self.getHttpResponseAndStatus(method, uri, params, extraHeaders = authHeader)

    def command(self, method, uri, params):
        data, code = self.getResponseAndStatus(method, uri, params)
        if self.response_as_string:
            return data, code
        return  ApiResponse(data, code), code
