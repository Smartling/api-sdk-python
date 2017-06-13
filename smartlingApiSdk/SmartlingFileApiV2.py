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

from .FileApiV2 import FileApiV2

class SmartlingFileApiV2(FileApiV2):
    """ Wrapper class providing access to all file API commands, all methods below represent API commands.
        Each command returns tuple = (response, status_code) 
        where response is ApiResponse object and status code = HTTP response status code
        
        ApiResponse object is python object as a result of json response parsing
        ApiResponse attributes depend on response json.
        To view all attributes of response use:
        for k,v in response.items(): print k, ':' ,v
        
        Response also can be a string to provide backward compatibility with previous versions
        in case you need json response as a string use :
        api = SmartlingFileApi(userIdentifier, userSecret, projectId)
        api.response_as_string = True
        
        Some of methods may be called with optional parameters
        like `list` method may have locale optional parameter or offset parameter
        simple list:
             api.list()
        list with additional parameters:
             api.list(limit=100, offset=50)
        """
        
    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None):
        FileApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings)

    def upload(self, filePath, fileType, **kw):
        """ Uploads original source content to Smartling
            returns (response, status_code) tuple
            for details on `upload` command see http://docs.smartling.com/pages/API/v2/FileAPI/Upload-File/ """
        return self.commandUpload(filePath, fileType, **kw)

    def get(self, fileUri, locale, **kw):
        """ implements `get` api command
            returns (response, status_code) tuple where response is file for specific locale
            for details on `get` command see http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/Single-Locale/ """
        return self.commandGet(fileUri, locale, **kw)
        
    def get_multiple_locales(self, fileUri, localeIds, directives={}, **kw):   
        """ downloads multiple locales of file(s) as zip
            returns (response, status_code) tuple where response is zip file
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/Multiple-Locales/ 

            if you wish to pass smartling.[command] use directives argument 
            for example smartling.placeholder_format_custom directive:
            directives={'placeholder_format_custom' : '\[.+?\]'}
            """
        return self.commandGetMultipleLocalesAsZip(fileUri, localeIds, directives, **kw)
        
    def get_all_locales(self, fileUri, directives={}, **kw):
        """ downloads all locales of file as zip
            returns (response, status_code) tuple where response is zip file
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/All-Locales/ 

            if you wish to pass smartling.[command] use directives argument 
            for example smartling.placeholder_format_custom directive:
            directives={'placeholder_format_custom' : '\[.+?\]'}
            """
        return self.commandGetAllLocalesZip(fileUri, directives, **kw)
        
    def get_all_locales_csv(self, fileUri, directives={}, **kw):
        """ downloads all translations for the requested file in a single CSV file
            returns (response, status_code) tuple where response is csv file
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/All-Locales-CSV/

            if you wish to pass smartling.[command] use directives argument 
            for example smartling.placeholder_format_custom directive:
            directives={'placeholder_format_custom' : '\[.+?\]'}
            """
        return self.commandGetAllLocalesCsv(fileUri, directives, **kw)      

    def get_original(self, fileUri):
        """ downloads the original version of the requested file from Smartling
            returns (response, status_code) tuple where response is csv file
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/Original-File/ """
        return self.commandGetOriginal(fileUri) 

    def list(self, **kw):
        """ implements `list` api command
            returns (response, status_code) tuple
            for details on `list` http://docs.smartling.com/pages/API/v2/FileAPI/List/ """
        return self.commandList(**kw)
        
    def list_file_types(self, **kw):
        """ Returns a list of all file types currently represented in the project.
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/List-File-Types/ """
        return self.commandListFileTypes(**kw) 
        
    def delete(self, fileUri, **kw):
        """ Removes the file from Smartling. The file will no longer be available for download. 
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Delete/ """
        return self.commandDelete(fileUri, **kw)        

    def status(self, fileUri):
        """ Returns information on a specific file.
            returns (response, status_code) tuple
            for details see  http://docs.smartling.com/pages/API/v2/FileAPI/Status/All-Locales/ """
        return self.commandStatus(fileUri)
        
    def status_locale(self, fileUri, locale):
        """ Returns detailed status information on a specific file.
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Status/Single-Locale/ """
        return self.commandStatusLocale(fileUri, locale)
        
    def rename(self, fileUri, newFileUrl):
        """ Renames an uploaded file by changing the fileUri.
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Rename/ """
        return self.commandRename(fileUri, newFileUrl)

    def last_modified(self, fileUri, localeId, **kw):
        """ Returns the date a file was last modified in a specified locale.
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Last-Modified/Single-Locale/ """
        return self.commandLastModified(fileUri, localeId, **kw)

    def last_modified_all(self, fileUri, **kw):
        """ Returns the date a file was last modified in a each locale
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Last-Modified/All-Locales/ """
        return self.commandLastModifiedAll(fileUri, **kw)    
        
    def import_call(self, fileUriOriginal, filePathTranslated, fileType, localeId, directives={}, **kw):
        """ Import Translations.
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Import-Translations/

            if you wish to pass smartling.[command] use directives argument 
            for example smartling.placeholder_format_custom directive:
            directives={'placeholder_format_custom' : '\[.+?\]'}
            """
        return self.commandImport(fileUriOriginal, filePathTranslated, fileType, localeId, directives, **kw)
        

    def list_authorized_locales(self, fileUri):
        """ Returns a list of locales the file is authorized for..
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Authorize-Content/List-Authorized-Locales """
        return self.commandListAuthorizedLocales(fileUri)
        
    def authorize(self, fileUri, localeIds):
        """ Authorize a file for translation in the specified locales.
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Authorize-Content/Authorize/ """
        return self.commandAuthorize(fileUri, localeIds)
        
    def unauthorize(self, fileUri, localeIds):
        """ Unauthorize a file for translation in the specified locales.
            returns (response, status_code) tuple
            for details see http://docs.smartling.com/pages/API/v2/FileAPI/Authorize-Content/Unauthorize/ / """
        return self.commandUnauthorize(fileUri, localeIds)
        
    def get_translations(self, fileUri, filePath, localeId, directives={}, **kw):
        """ Temporarily uploads a file, then returns a translated version for requested locales.
            returns (response, status_code) tuple
            for http://docs.smartling.com/pages/API/v2/FileAPI/Get-Translations/

            if you wish to pass smartling.[command] use directives argument 
            for example smartling.placeholder_format_custom directive:
            directives={'placeholder_format_custom' : '\[.+?\]'}
            """
        return self.commandGetTranslations(fileUri, filePath, localeId, directives, **kw)
