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
    def __init__(self, dict):
        self.dict = dict
        
    def __getattr__(self, key):
        return self.dict[key]
        
    def __str__(self):
        return `self.dict`

class ApiResponse:
    def __init__(self, response_string, status_code):
        self.status_code = status_code
        self.response_string = response_string
        self.parse_response(response_string)
        
    def parse_response(self, response_string):
        self.response_dict = json.loads(response_string)
        print self.response_dict
        for k, v in self.response_dict['response'].items():
            if k=='data':
                self.data = Data(v)
            else:
                setattr(self, k, v)

    def __str__(self):
        return self.response_string
        
    def __getattr__(self, key):
        try:
            return getattr(self, key)
        except:
            return getattr(self.response_string, key)