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

from FileApiBase import FileApiBase


class SmartlingFileApi(FileApiBase):

    def __init__(self, host, apiKey, projectId):
        FileApiBase.__init__(self, host, apiKey, projectId)

    def upload(self, uploadData):
        return self.commandUpload(uploadData)

    def list(self, **kw):
        return self.commandList(**kw)

    def get(self, fileUri, locale, **kw):
        return self.commandGet(fileUri, locale, **kw)

    def status(self, fileUri, locale, **kw):
        return self.commandStatus(fileUri, locale, **kw)

    def rename(self, fileUri, newUri, **kw):
        return self.commandRename(fileUri, newUri, **kw)

    def delete(self, fileUri, **kw):
        return self.commandDelete(fileUri, **kw)

    def import_call(self, uploadData, locale, **kw):
        return self.commandImport(uploadData, locale, **kw)
        
    def last_modified(self, fileUri, locale=None, **kw):
        return self.commandLastModified(fileUri, **kw)
    

class SmartlingFileApiFactory:
    sandbox_host = 'sandbox-api.smartling.com'
    api_host = 'api.smartling.com'

    def getSmartlingTranslationApi(self, productionMode, apiKey, projectId):
        if (productionMode):
            return SmartlingFileApi(self.api_host, apiKey, projectId)
        return SmartlingFileApi(self.sandbox_host, apiKey, projectId)

    def getSmartlingTranslationApiProd(self, apiKey, projectId):
        return SmartlingFileApi(self.api_host, apiKey, projectId)

