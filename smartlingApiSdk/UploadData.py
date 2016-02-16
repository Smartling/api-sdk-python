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

#properties for upload


class UploadData:
    """ Helper class to store `upload` and `import` command attributes """
    approveContent = "false"
    callbackUrl = ""
    localesToApprove = []

    def __init__(self, path, name, type):
        self.path = path
        self.name = name
        self.type = type
        self.uri  = name
        self.directives = []
 
    def setApproveContent(self, approveContent):
        self.approveContent = approveContent

    def setCallbackUrl(self, callbackUrl):
        self.callbackUrl = callbackUrl
        
    def setLocalesToApprove(self, localesToApprove):
        self.localesToApprove = localesToApprove

    def addDirective(self, directive):
        self.directives.append(directive)

    def setUri(self, uri):
        self.uri = uri
