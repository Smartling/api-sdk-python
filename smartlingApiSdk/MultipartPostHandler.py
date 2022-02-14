#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012 Smartling, Inc.
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

import sys

isPython3 =  sys.version_info[:2] >= (3,0)

if isPython3:
    import email.generator as mimetools
    import urllib.request as urllib2
    from urllib.parse import urlencode
else:
    import mimetools
    import urllib2
    from urllib import urlencode

import mimetypes
import io

class MultipartPostHandler(urllib2.BaseHandler):
    """ handler for multipart HTTP POST, helper object to provide POST functionality """

    handler_order = urllib2.HTTPHandler.handler_order - 10  # needs to run first
    # Controls how sequences are uncoded. If true, elements may be given multiple values by
    #  assigning a sequence.
    doseq = 1

    def ifFileInstance(self, value):
        if isPython3:
            return isinstance(value, io.IOBase) or type(value) == io.StringIO
        else:
            return type(value) == file or type(value) == io.StringIO

    def http_request(self, request, forceMultipart = False):
        if isPython3:
            data = request.data
        else:
            data = request.get_data()
            try: data = data.encode('utf-8', 'ignore')
            except: pass
        if data is not None and type(data) != str and type(data) != bytes:
            files = []
            vars = []
            try:
                for(key, value) in list(data.items()):
                    if self.ifFileInstance(value):
                        files.append((key, value))
                    else:
                        vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError("not a valid non-string sequence or mapping object")(traceback)

            if (not forceMultipart) and len(files) == 0:
                data = urlencode(vars, self.doseq)
            else:
                boundary, data = self.multipartEncode(vars, files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary

                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print("Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data'))
                request.add_unredirected_header('Content-Type', contenttype)
                request.headers["Content-type"] = contenttype

            if isPython3:
                request.data = data
            else:
                request.add_data(data)
        return request

    def multipartEncode(self, vars, files):
        boundary = self.createBoundary()

        buffer = ''
        for(key, value) in vars:
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"' % key
            buffer += '\r\n\r\n' + value + '\r\n'
        for(key, fd) in files:
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename)
            buffer += 'Content-Type: %s\r\n' % contenttype
            fd.seek(0)
            if isPython3:
                fileData = fd.read()
                if type(fileData) is str :
                    fileData = fileData.encode()
                buffer = buffer.encode() + b'\r\n' + fileData + b'\r\n'
            else:
                buffer += '\r\n' + fd.read() + '\r\n'

        if isPython3:
            if str == type(buffer):
                buffer = buffer.encode()
            buffer += b'--%b--\r\n\r\n' % boundary.encode()
        else:
            buffer += '--%s--\r\n\r\n' % boundary
        return boundary, buffer

    def createBoundary(self):
        if isPython3:
            boundary = mimetools._make_boundary()
            boundary = boundary.replace("=", "-")
        else:
            boundary = mimetools.choose_boundary()
        return boundary

    https_request = http_request
