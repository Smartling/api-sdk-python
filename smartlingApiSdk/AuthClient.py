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

from HttpClient import HttpClient
from ApiResponse import ApiResponse
import time
from Constants import ReqMethod
import pdb
class AuthClient:
    host = "api.smartling.com"
    authUri = "/auth-api/v2/authenticate"
    refreshUri = "/auth-api/v2/authenticate/refresh"
    timeJitter = 5 #seconds off server expires time

    def __init__(self, userIdentifier, userSecret, proxySettings=None):
        self.httpClient = HttpClient(self.host, proxySettings)
        self.userIdentifier = userIdentifier
        self.userSecret = userSecret
        
    def request(self, uri, body):
        header = {"Content-Type": "application/json"}
        response_data, status_code = self.httpClient.getHttpResponseAndStatus(ReqMethod.POST, uri, params={}, extraHeaders=header, requestBody=body)
        apiResponse = ApiResponse(response_data, status_code)
        
        now = time.time()
        try:
            self.accessToken = apiResponse.data.accessToken
            self.refreshToken = apiResponse.data.refreshToken
            self.accessExpiresAt = now + apiResponse.data.expiresIn - self.timeJitter
            self.refreshExpiresAt = now + apiResponse.data.refreshExpiresIn - self.timeJitter
        except Exception, e:
            print e
            self.accessToken = None
        
    def authenticate(self):
        body = '{"userIdentifier": "%s", "userSecret": "%s"}' % (self.userIdentifier, self.userSecret)
        self.request(self.authUri, body)
        
    def refresh(self):
        body = '{"refreshToken":"%s"}' % self.refreshToken 
        self.request(self.refreshUri, body)
        
    def getToken(self):
        if not hasattr(self,'accessToken'):
            self.authenticate()
        
        now = time.time()
        if now >= self.accessExpiresAt:
            if now >= self.refreshExpiresAt:
               self.refresh()
            else:
                self.authenticate()
        return self.accessToken 
