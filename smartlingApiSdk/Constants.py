#!/usr/bin/python
# -*- coding: utf-8 -*-




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
    PUT    = "PUT"


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
