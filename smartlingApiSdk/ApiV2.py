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

# FileApi class implementation

from .AuthClient import AuthClient
from .Constants import FileTypes
from .Constants import Params
from .FileApiBase import FileApiBase
from .SmartlingDirective import SmartlingDirective
from .UrlV2Helper import UrlV2Helper
from .version import version


class ApiV2(FileApiBase):
    """ Api v2 basic functionality """
    hostProd = 'api.smartling.com'
    hostStg = 'api.stg.smartling.net'
    clientUid = "{\"client\":\"smartling-api-sdk-python\",\"version\":\"%s\"}" % version

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        self.host = self.hostProd
        self.userIdentifier = userIdentifier
        if 'stg'==env:
            self.host = self.hostStg
        FileApiBase.__init__(self, self.host, userIdentifier, userSecret, proxySettings, permanentHeaders=permanentHeaders)
        self.authClient = AuthClient(self.host, userIdentifier, userSecret, proxySettings)
        self.urlHelper = UrlV2Helper(projectId)

    def addAuth(self, params):
        token = self.authClient.getToken()
        if token is None:
            raise Exception("Error getting token, userIdentifier:%s" % (self.userIdentifier))
        return {"Authorization": "Bearer " + token}

    def validateFileTypes(self, kw):
        fileTypes = kw.get("fileTypes", [])
        if type(fileTypes) != type([]) and type(fileTypes) != type(()):
            fileTypes = [fileTypes]
        for t in fileTypes:
            if not getattr(FileTypes, t, None):
                unsupported = "\nUnsupported file type:%s\n" % t
                raise Exception(unsupported)

    def checkRetrievalType(self, kw):
        if Params.RETRIEVAL_TYPE in kw and not kw[Params.RETRIEVAL_TYPE] in Params.allowedRetrievalTypes:
            Exception("Not allowed value `%s` for parameter:%s try one of %s" % (kw[Params.RETRIEVAL_TYPE],
                                                                                 Params.RETRIEVAL_TYPE,
                                                                                 Params.allowedRetrievalTypes))

    def processDirectives(self, params, directives):
        for name, value in list(directives.items()):
            params[SmartlingDirective.SL_PREFIX + name] = value

    def addLibIdDirective(self, params):
        name = "client_lib_id"
        params[SmartlingDirective.SL_PREFIX + name] = self.clientUid
