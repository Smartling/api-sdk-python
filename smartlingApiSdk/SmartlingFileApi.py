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

from .FileApiBase import FileApiBase


class SmartlingFileApi(FileApiBase):
    """ Wrapper class providing access to all file API commands, all methods below represent API commands.
        Each command returns tuple = (response, status_code) 
        where response is ApiResponse object and status code = HTTP response status code
        
        ApiResponse object is python object as a result of json response parsing
        ApiResponse attributes depend on response json.
        To view all attributes of response use:
        for k,v in response.items(): print k, ':' ,v
        
        Response also can be a string to provide backward compatibility with previous versions
        in case you need json response as a string use :
        api = SmartlingFileApi(host, apiKey, projectId)
        api.response_as_string = True
        
        Some of methods may be called with optional parameters
        like `list` method may have locale optional parameter or offset parameter
        simple list:
             api.list()
        list with additional parameters:
             api.list(locale='es-ES', offset=50)
        """

    def __init__(self, host, apiKey, projectId, proxySettings=None):
        FileApiBase.__init__(self, host, apiKey, projectId, proxySettings)

    def upload(self, uploadData):
        """ implements `upload` api command
            returns (response, status_code) tuple
            for python 2.5 and less commands `upload` and `import_call` returns status_code 0
            for details on `upload` command see  https://docs.smartling.com/display/docs/Files+API#FilesAPI-/file/upload%28POST) """
        return self.commandUpload(uploadData)

    def list(self, **kw):
        """ implements `list` api command
            returns (response, status_code) tuple
            for details on `list` command see https://docs.smartling.com/display/docs/Files+API#FilesAPI-/file/list%28GET%29 """
        return self.commandList(**kw)

    def get(self, fileUri, locale, **kw):
        """ implements `get` api command
            returns (response, status_code) tuple
            for details on `get` command see https://docs.smartling.com/display/docs/Files+API#FilesAPI-/file/list%28GET%29 """
        return self.commandGet(fileUri, locale, **kw)

    def status(self, fileUri, locale, **kw):
        """ implements `status` api command
            returns (response, status_code) tuple
            for details on `status` command see  https://docs.smartling.com/display/docs/Files+API#FilesAPI-/file/status%28GET) """
        return self.commandStatus(fileUri, locale, **kw)

    def rename(self, fileUri, newUri, **kw):
        """ implements `rename` api command
            returns (response, status_code) tuple
            for details on `rename` command see  https://docs.smartling.com/display/docs/Files+API#FilesAPI-/file/rename%28POST) """
        return self.commandRename(fileUri, newUri, **kw)

    def delete(self, fileUri, **kw):
        """ implements `delete` api command
            returns (response, status_code) tuple
            for details on `delete` command see https://docs.smartling.com/display/docs/Files+API#FilesAPI-/file/delete%28DELETE%29 """
        return self.commandDelete(fileUri, **kw)

    def import_call(self, uploadData, locale, **kw):
        """ implements `import` api command
            returns (response, status_code) tuple
            for python 2.5 and less commands `upload` and `import_call` returns status_code 0
            for details on `import` command see https://docs.smartling.com/display/docs/Files+API#FilesAPI-/file/import%28POST%29 """
        return self.commandImport(uploadData, locale, **kw)
        
    def last_modified(self, fileUri, locale=None, **kw):
        """ implements `last_modified` api command
            returns (response, status_code) tuple
            for details on `last_modified` command see https://docs.smartling.com/display/docs/Files+API#FilesAPI-/file/last_modified%28GET%29 """
        return self.commandLastModified(fileUri, **kw)
    

class SmartlingFileApiFactory:
    """ Factory class to build SmartlingFileApi objects """
    api_host = 'api.smartling.com'

    def getSmartlingTranslationApi(self, apiKey, projectId, proxySettings=None):
        return SmartlingFileApi(self.api_host, apiKey, projectId, proxySettings)
