#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012-2025 Smartling, Inc.
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

from .HttpClient import HttpClient

from .Constants import Params, ReqMethod
from .ApiResponse import ApiResponse
import logging
import json
from pathlib import Path


class FileApiBase:
    """ basic class implementing low-level api calls """
    

    def __init__(self, host, proxySettings=None, permanentHeaders={}):
        self.host = host
        self.proxySettings = proxySettings
        self.httpClient = HttpClient(host, proxySettings, permanentHeaders=permanentHeaders)

    

    def processFile(self, file_content: str | Path):
        """Returns a file-like object from a string or file path.
        Tries to treat string as file path or make it file-like object to be uploaded.
        """
        if isinstance(file_content, Path):
            return open(file_content, 'rb')
        elif isinstance(file_content, str):
            f = io.StringIO(file_content)
            f.seek(0)
            f.name = 'String'
            return f
        else:
            return file_content

    def filterOutDefaults(self, params):
        if hasattr(params, 'items'):
            keys_to_delete = []
            for k, v in list(params.items()):
                if k == 'namespace':
                    continue
                if isinstance(v, bool): 
                    continue
                if not v:
                    keys_to_delete.append(k)
            for k in keys_to_delete:
                del params[k]

    def uploadMultipart(self, uri, params):
        self.filterOutDefaults(params)
        authHeader = self.addAuth(params)
        if Params.FILE_PATH in params:
            params[Params.FILE] = open(params[Params.FILE_PATH], 'rb')
            del params[Params.FILE_PATH]  # no need in extra field in POST

        response_data, status_code, headers = self.getHttpResponseAndStatus(ReqMethod.POST ,uri, params, extraHeaders = authHeader)
        response_data = response_data.strip()
        if not self.isJsonResponse(headers):
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
            logging.error("code:%d RequestId:%s jsonBody=%s" % (code, rId, jsonBody))


        if not self.isJsonResponse(headers):

    def getHttpResponseAndStatus(self, method, uri, params, extraHeaders = None):
        return self.httpClient.getHttpResponseAndStatus(method, uri, params, extraHeaders = extraHeaders)
  
    def getResponseAndStatus(self, method, uri, params):
        authHeader = self.addAuth(params)
        return self.getHttpResponseAndStatus(method, uri, params, extraHeaders = authHeader)

    def isJsonResponse(self, headers):
        hdr = 'Content-Type'
        return 'json' in headers.get(hdr,'')

    def command(self, method, uri, params):
        self.filterOutDefaults(params)
        data, code, headers = self.getResponseAndStatus(method, uri, params)
        if not self.isJsonResponse(headers):
            return data, code
        result = ApiResponse(data, code, headers)
        if result.isApiResonse:
            return result, code
        return data, code
