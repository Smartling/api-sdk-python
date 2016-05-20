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

#constants for File API

class Params:
    allowedRetrievalTypes = ('pending', 'published', 'pseudo', 'contextMatchingInstrumented')

    API_KEY    = 'apiKey'
    PROJECT_ID = 'projectId'
    FILE_PATH  = 'file_path'
    FILE_URI   = 'fileUri'
    FILE_TYPE  = 'fileType'
    LOCALE     = 'locale'
    FILE       = 'file'
    APPROVED   = 'approved'
    RETRIEVAL_TYPE = 'retrievalType'
    FILE_URI_NEW   = 'newFileUri'
    CALLBACK_URL    = 'callbackUrl'
    LOCALES_TO_APPROVE = 'localesToApprove'
    LOCALE_IDS = 'localeIds'
    LOCALE_IDS_BRACKET = 'localeIds[]'
    FILE_URIS   = 'fileUris'

class Uri:
    base = '/v1/file/'
    UPLOAD = base + 'upload'
    LIST   = base + 'list'
    GET    = base + 'get'
    STATUS = base + 'status'
    DELETE = base + 'delete'
    RENAME = base + 'rename'
    IMPORT = base + 'import'
    LAST_MODIFIED = base + 'last_modified'

class ReqMethod:
    POST   = "POST"
    GET    = "GET"
    DELETE = "DELETE"

class FileTypes:
    android        = "android"
    ios            = "ios"
    gettext        = "gettext"
    html           = "html"
    javaProperties = "javaProperties"
    yaml           = "yaml"
    xliff          = "xliff"
    xml            = "xml"
    json           = "json"
    docx           = "docx"
    pptx           = "pptx"
    xlsx           = "xlsx"
    idml           = "idml"
    qt             = "qt"
    resx           = "resx"
    plaintext      = "plaintext"
    cvs            = "cvs"
