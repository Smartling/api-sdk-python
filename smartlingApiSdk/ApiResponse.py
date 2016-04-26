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

try:
    import json
except ImportError:
    import simplejson24 as json
    
class Data:
    """ provides dictionary items to be object attributes """
    def __init__(self, dict):
        self.dict = dict
        
    def __getattr__(self, key):
        return self.dict[key]
        
    def __str__(self):
        return `self.dict`

class ApiResponse:
    """ response object to store parsed json response as python object, it also behaves like string for backward 
        compatibility with previous SDK versions where response was a string """
    def __init__(self, response_string, status_code):
        self.status_code = status_code
        self.response_string = response_string
        #print status_code, response_string
        self.parse_response(response_string)
        
    def parse_response(self, response_string):
        """ parses json and fills object attributes according json attributes """
        self.response_dict = json.loads(response_string)
        for k, v in self.response_dict['response'].items():
            if k=='data':
                self.data = Data(v)
            else:
                setattr(self, k, v)
    
    def __getattr__(self, key):
        """ provides string object methods to be available for response to behave like a string """
        if hasattr(self.response_dict, key):
            return getattr(self.response_string, key)
            
        try:
            return getattr(self, key)
        except:
            return getattr(self.response_string, key)