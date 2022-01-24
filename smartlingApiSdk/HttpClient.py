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

import sys

isPython3 = sys.version_info[:2] >= (3,0)

if isPython3:
    import urllib.request as urllib2
    import urllib.error
    HTTPError = urllib.error.HTTPError
    from urllib.parse import urlencode
else:
    import urllib, urllib2
    HTTPError = urllib2.HTTPError
    from urllib import urlencode

from .Constants import ReqMethod
from .Settings import Settings
from .MultipartPostHandler import MultipartPostHandler
import ssl

class HttpClient:
    protocol = 'https://'

    def __init__(self, host, proxySettings=None, permanentHeaders={}):
        self.host = host
        self.proxySettings = proxySettings
        self.permanentHeaders = permanentHeaders
        self.ignore_errors = False
        self.list_brackets = True  # Add [] suffix to GET list keys in urls, like &hashcodes[]=abcd, required by Files API
        self.force_multipart = True

    def getHttpResponseAndStatus(self, method, uri, params, handler=None, extraHeaders={}, requestBody="", context=None):
        self.installOpenerWithProxy(handler)
        if handler:
            prarms = self.encodeListParams(params)
        else:
            params = self.encodeParametersAsString(params)

        headers = {"User-Agent": Settings.userAgent}
        for k, v in list(extraHeaders.items())+list(self.permanentHeaders.items()):
            headers[k] = v
        headers = self.setContentType(method, headers)

        url = self.protocol + self.host + uri
        if method in (ReqMethod.GET, ReqMethod.DELETE) and params:
            url += "?" + params
        req = urllib2.Request(url, params, headers=headers)
        req.get_method = lambda: method

        try:
            if requestBody:
                response = urllib2.urlopen(req, requestBody, context=context)
            else:
                if handler:
                    multipartHandler = MultipartPostHandler()
                    req = multipartHandler.http_request(req, self.force_multipart)
                else:
                    req.data = req.data.encode()
                response = urllib2.urlopen(req, timeout=Settings.requestTimeoutSeconds, context=context)
        except HTTPError as e:
            response = e

        except Exception as e:
            if type(getattr(e, "reason", None)) == getattr(ssl,'SSLCertVerificationError', None):
                raise Exception("\nSome python versions require installation of local ssl certificate!\nuse command:\npip install certifi\nor on macos run command:\nopen /Applications/Python*/Install\ Certificates.command")
            raise e

        if sys.version_info[:2] >= (2, 6):
            status_code = response.getcode()
        else:
            status_code = response.code

        headers = dict(response.info())

        response_data = response.read()
        if status_code not in [200, 202] and not self.ignore_errors:
            print("Non 200 response:%s   RequestId:%s   URL:%s   response:%s" %
                  (status_code, headers.get("X-SL-Requestid","Unknown"), url, response_data)
                 )
        return response_data, status_code, headers

    def installOpenerWithProxy(self, handler):
        if self.proxySettings:
            if self.proxySettings.username:
                proxyStr = 'http://%s:%s@%s:%s' % (
                self.proxySettings.username, self.proxySettings.passwd, self.proxySettings.host,
                self.proxySettings.port)
            else:
                proxyStr = 'http://%s:%s' % (self.proxySettings.host, self.proxySettings.port)

            opener = urllib2.build_opener(
                handler or urllib2.HTTPHandler(),
                handler or urllib2.HTTPSHandler(),
                urllib2.ProxyHandler({"https": proxyStr}))
            urllib2.install_opener(opener)
        elif handler:
            opener = urllib2.build_opener(MultipartPostHandler)
            urllib2.install_opener(opener)

    def encodeParametersAsString(self, params):
        #processes list parameters separately i.e. {key:[v1, v2]} is encoded as 'key[]=v1&key[]=v2'
        result = ""
        for k, v in list(params.items()):
            if type(v) == bool: params[k] = str(v).lower()
            if type(v) == type([]) or type(v) == type(()):
                del params[k]
                for single in v:
                    if len(result) > 0:
                        result += "&"
                    keyList = k
                    if self.list_brackets:
                        keyList += "[]"
                    dct = {keyList: single}
                    result += urlencode(dct)

        if params:
            if len(result) > 0:
                result += "&"

            result += urlencode(params)

        return result

    def encodeListParams(self, params):
        for k, v in list(params.items()):
            if type(v) == bool:
                params[k] = str(v).lower()
            if type(v) == type([]) or type(v) == type(()):
                del params[k]
                params[k + '[]'] = ",".join(v)
        return params

    def setContentType(self, method, headers):
        ct = "Content-Type"
        if method in (ReqMethod.POST, ReqMethod.PUT) and ct not in headers:
            headers[ct] = "application/x-www-form-urlencoded"
        return headers
