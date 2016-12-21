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

class UrlV2Helper:
    
    GET = "/files-api/v2/projects/{projectId}/locales/{localeId}/file"
    GET_MULTIPLE_LOCALES = "/files-api/v2/projects/{projectId}/files/zip"
    GET_ALL_LOCALES_ZIP = "/files-api/v2/projects/{projectId}/locales/all/file/zip"
    GET_ALL_LOCALES_CSV = "/files-api/v2/projects/{projectId}/locales/all/file"
    GET_ORIGINAL = "/files-api/v2/projects/{projectId}/file"
    LIST_FILES = "/files-api/v2/projects/{projectId}/files/list"
    LIST_FILE_TYPES = "/files-api/v2/projects/{projectId}/file-types"
    UPLOAD = "/files-api/v2/projects/{projectId}/file"
    DELETE = "/files-api/v2/projects/{projectId}/file/delete"
    PROJECT_DETAILS = "/projects-api/v2/projects/{projectId}"
    PROJECTS = "/accounts-api/v2/accounts/{accountUid}/projects"
    STATUS_ALL = "/files-api/v2/projects/{projectId}/file/status"
    STATUS_LOCALE = "/files-api/v2/projects/{projectId}/locales/{localeId}/file/status"
    RENAME = "/files-api/v2/projects/{projectId}/file/rename"
    LAST_MODIFIED = "/files-api/v2/projects/{projectId}/locales/{localeId}/file/last-modified"
    LAST_MODIFIED_ALL = "/files-api/v2/projects/{projectId}/file/last-modified"
    IMPORT = "/files-api/v2/projects/{projectId}/locales/{localeId}/file/import"
    LIST_AUTHORIZED_LOCALES = "/files-api/v2/projects/{projectId}/file/authorized-locales"
    AUTHORIZE = "/files-api/v2/projects/{projectId}/file/authorized-locales"
    UNAUTHORIZE = "/files-api/v2/projects/{projectId}/file/authorized-locales"
    GET_TRANSLATIONS = "/files-api/v2/projects/{projectId}/locales/{localeId}/file/get-translations"
    
    def __init__(self, projectId):
        self.projectId = projectId

    def getUrl(self, urlWithPlaceholders, localeId="", accountUid="", projectId=""):
        
        url = urlWithPlaceholders
        if self.projectId:
            url = url.replace("{projectId}", self.projectId)
        elif projectId:
            url = url.replace("{projectId}", projectId)

        if localeId : 
            url = url.replace("{localeId}", localeId)
        
        if accountUid : 
            url = url.replace("{accountUid}", accountUid)
        
        if "{localeId}" in url:
            raise "Unhandled localeId placeholder:" + url
            
        if "{accountUid}" in url:
            raise "Unhandled accountUid placeholder:" + url
            
        if "{projectId}" in url:
            raise "Unhandled projectId placeholder:" + url
            
        return url