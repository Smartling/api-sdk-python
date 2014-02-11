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

import httplib
import urllib
import urllib2
from MultipartPostHandler import MultipartPostHandler
from Constants import Uri, Params, ReqMethod


class FileApiBase:
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    def __init__(self, host, apiKey, projectId):
        self.host = host
        self.apiKey = apiKey
        self.projectId = projectId

    def addApiKeys(self, params):
        params[Params.API_KEY] = self.apiKey
        params[Params.PROJECT_ID] = self.projectId

    def uploadMultipart(self, params):
        self.addApiKeys(params)
        params[Params.FILE] = open(params[Params.FILE_PATH], 'rb')
        del params[Params.FILE_PATH]  # no need in extra field in POST
        opener = urllib2.build_opener(MultipartPostHandler)
        urllib2.install_opener(opener)
        req = urllib2.Request('https://' + self.host + Uri.UPLOAD, params)
        response = urllib2.urlopen(req).read().strip()
        return response

    def command(self, method, uri, params):
        self.addApiKeys(params)
        params_encoded = urllib.urlencode(params)
        conn = httplib.HTTPSConnection(self.host)
        conn.request(method, uri, params_encoded, self.headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data, response.status

    # commands

    def commandUpload(self, uploadData):
        params = {
                    Params.FILE_URI: uploadData.name,
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

        return self.uploadMultipart(params)

    def commandList(self, **kw):
        return self.command(ReqMethod.POST, Uri.LIST, kw)

    def commandGet(self, fileUri, locale, **kw):
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE] = locale
        if Params.RETRIEVAL_TYPE in kw and not kw[Params.RETRIEVAL_TYPE] in Params.allowedRetrievalTypes:
            raise "Not allowed value `%s` for parameter:%s try one of %s" % (kw[Params.RETRIEVAL_TYPE],
                                                                             Params.RETRIEVAL_TYPE,
                                                                             Params.allowedRetrievalTypes)

        return self.command(ReqMethod.POST, Uri.GET, kw)

    def commandDelete(self, fileUri, **kw):
        kw[Params.FILE_URI] = fileUri

        return self.command(ReqMethod.POST, Uri.DELETE, kw)

    def commandStatus(self, fileUri, locale, **kw):
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE] = locale

        return self.command(ReqMethod.POST, Uri.STATUS, kw)

    def commandRename(self, fileUri, newUri, **kw):
        kw[Params.FILE_URI] = fileUri
        kw[Params.FILE_URI_NEW] = newUri

        return self.command(ReqMethod.POST, Uri.RENAME, kw)
