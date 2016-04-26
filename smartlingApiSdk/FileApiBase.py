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

class FileApiBase:
    """ basic class implementing low-level api calls """
    response_as_string = False

    def __init__(self, host, apiKey, projectId, proxySettings=None):
        self.host = host
        self.apiKey = apiKey
        self.projectId = projectId
        self.proxySettings = proxySettings
        self.httpClient = HttpClient(host, proxySettings)

    def addApiKeys(self, params):
        params[Params.API_KEY] = self.apiKey
        params[Params.PROJECT_ID] = self.projectId

    def uploadMultipart(self, uri, params):
        self.addApiKeys(params)
        params[Params.FILE] = open(params[Params.FILE_PATH], 'rb')
        del params[Params.FILE_PATH]  # no need in extra field in POST
        response_data, status_code = self.getHttpResponseAndStatus( ReqMethod.POST, uri, params, MultipartPostHandler)
        response_data = response_data.strip()
        if self.response_as_string:
            return response_data, status_code
        return ApiResponse(response_data, status_code), status_code
  
    def getHttpResponseAndStatus(self, method, uri, params, handler=None):
        return self.httpClient.getHttpResponseAndStatus(method, uri, params, handler)
  
    def command_raw(self, method, uri, params):
        self.addApiKeys(params)
        return self.getHttpResponseAndStatus(method, uri, params)

    def command(self, method, uri, params):
        data, code = self.command_raw(method, uri, params)
        if self.response_as_string:
            return data, code
        return  ApiResponse(data, code), code

    # commands

    def commandUpload(self, uploadData):
        params = {
                    Params.FILE_URI: uploadData.uri or uploadData.name,
                    Params.FILE_TYPE: uploadData.type,
                    Params.FILE_PATH: uploadData.path + uploadData.name
                  }
        if (uploadData.approveContent):
            params[Params.APPROVED] = uploadData.approveContent

        if (uploadData.callbackUrl):
            params[Params.CALLBACK_URL] = uploadData.callbackUrl

        if (uploadData.directives):
            for index, directive in enumerate(uploadData.directives):
                params[directive.sl_prefix + directive.name] = directive.value
                
        if (uploadData.localesToApprove):
            for index, locale in enumerate(uploadData.localesToApprove):
                params['{0}[{1}]'.format(Params.LOCALES_TO_APPROVE, index)] = locale

        return self.uploadMultipart(Uri.UPLOAD, params)

    def commandList(self, **kw):
        return self.command(ReqMethod.POST, Uri.LIST, kw)

    def commandLastModified(self, fileUri, locale=None, **kw):
        kw[Params.FILE_URI] = fileUri
        if locale is not None:
            kw[Params.LOCALE] = locale
        return self.command(ReqMethod.GET, Uri.LAST_MODIFIED, kw)
        
    def commandGet(self, fileUri, locale, **kw):
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE] = locale
        if Params.RETRIEVAL_TYPE in kw and not kw[Params.RETRIEVAL_TYPE] in Params.allowedRetrievalTypes:
            raise "Not allowed value `%s` for parameter:%s try one of %s" % (kw[Params.RETRIEVAL_TYPE],
                                                                             Params.RETRIEVAL_TYPE,
                                                                             Params.allowedRetrievalTypes)

        return self.command_raw(ReqMethod.POST, Uri.GET, kw)

    def commandDelete(self, fileUri, **kw):
        kw[Params.FILE_URI] = fileUri

        return self.command(ReqMethod.POST, Uri.DELETE, kw)
        
    def commandImport(self, uploadData, locale, **kw):
        kw[Params.FILE_URI]  = uploadData.uri
        kw[Params.FILE_TYPE] = uploadData.type
        kw[Params.FILE_PATH] = uploadData.path + uploadData.name
        kw["file"] = uploadData.path + uploadData.name + ";type=text/plain"
        kw[Params.LOCALE] = locale
        self.addApiKeys(kw)

        return self.uploadMultipart(Uri.IMPORT, kw)

    def commandStatus(self, fileUri, locale, **kw):
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE] = locale

        return self.command(ReqMethod.POST, Uri.STATUS, kw)

    def commandRename(self, fileUri, newUri, **kw):
        kw[Params.FILE_URI] = fileUri
        kw[Params.FILE_URI_NEW] = newUri

        return self.command(ReqMethod.POST, Uri.RENAME, kw)
