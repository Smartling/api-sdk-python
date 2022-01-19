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

#FileApi class implementation

from .HttpClient import HttpClient, isPython3
from .MultipartPostHandler import MultipartPostHandler
from .Constants import Params, ReqMethod
from .ApiResponse import ApiResponse
from .Logger import Logger
from .Settings import Settings
import io
import sys
import logging
import json


class FileApiBase:
    """ basic class implementing low-level api calls """
    response_as_string = False

    def __init__(self, host, apiKey, projectId, proxySettings=None, permanentHeaders={}):
        self.host = host
        self.apiKey = apiKey
        self.projectId = projectId
        self.proxySettings = proxySettings
        self.httpClient = HttpClient(host, proxySettings, permanentHeaders=permanentHeaders)
        sys.stdout = Logger('python-sdk', Settings.logLevel, Settings.logPath)
        sys.stderr = Logger('STDERR', logging.ERROR, Settings.logPath)

    def addAuth(self, params):
        params[Params.API_KEY] = self.apiKey
        params[Params.PROJECT_ID] = self.projectId
        return {}

    def processFile(self, file):
        """"
            returns file-like object form string or file
            tries to treat string as file path or make it file-like object to be uploaded
        """
        if not file or file==type(file):
            return file
        try:
            f = open(file, 'rb')
        except:
            f = io.StringIO(file)
            f.seek(0)
            f.name = 'String'
        return f

    def filterOutDefaults(self, params):
        if hasattr(params, 'items'):
            for k, v in list(params.items()):
                if k == 'namespace':
                    continue #when namespace is not specified it's replaced with 'smartling.strings-api.default.namespace' for strings api
                if bool == type(v): continue
                if not v: del params[k]
                if k == 'projectId': del params[k]

    def uploadMultipart(self, uri, params, response_as_string=False):
        self.filterOutDefaults(params)
        authHeader = self.addAuth(params)
        if Params.FILE_PATH in params:
            params[Params.FILE] = open(params[Params.FILE_PATH], 'rb')
            del params[Params.FILE_PATH]  # no need in extra field in POST

        response_data, status_code, headers = self.getHttpResponseAndStatus(ReqMethod.POST ,uri, params, MultipartPostHandler, extraHeaders = authHeader)
        response_data = response_data.strip()
        if self.response_as_string or response_as_string or not self.isJsonResponse(headers):
            return response_data, status_code
        return ApiResponse(response_data, status_code, headers), status_code

    def commandJson(self, method, uri, params):
        authHeader = self.addAuth(params)
        authHeader['Content-Type'] = 'application/json'
        self.filterOutDefaults(params)
        jsonBody = json.dumps(params).encode('utf8')

        data, code, headers = self.httpClient.getHttpResponseAndStatus(method, uri, params={}, requestBody = jsonBody, extraHeaders = authHeader)
        if not code in [200,202]:
            rId = headers.get("X-SL-RequestId","Unknown")
            print ("code:%d RequestId:%s jsonBody=%s" % (code, rId, jsonBody))


        if self.response_as_string or not self.isJsonResponse(headers):
            return data, code
        return  ApiResponse(data, code, headers), code

    def getHttpResponseAndStatus(self, method, uri, params, handler=None, extraHeaders = None):
        return self.httpClient.getHttpResponseAndStatus(method, uri, params, handler, extraHeaders = extraHeaders)
  
    def getResponseAndStatus(self, method, uri, params):
        authHeader = self.addAuth(params)
        return self.getHttpResponseAndStatus(method, uri, params, extraHeaders = authHeader)

    def isJsonResponse(self, headers):
        if isPython3:
            hdr = 'Content-Type'
        else:
            hdr = 'content-type'
        return 'json' in headers.get(hdr,'')

    def command(self, method, uri, params):
        self.filterOutDefaults(params)
        data, code, headers = self.getResponseAndStatus(method, uri, params)
        if self.response_as_string or not self.isJsonResponse(headers):
            return data, code
        result = ApiResponse(data, code, headers)
        if result.isApiResonse:
            return result, code
        return data, code
