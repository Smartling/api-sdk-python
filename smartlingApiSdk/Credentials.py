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
import os

class CredentialsNotSet(Exception):
    noKeymessage = """ 
     don't forget to set real MY_PROJECT_ID, MY_USER_IDENTIFIER, MY_USER_SECRET, MY_LOCALE
     in Credentials class
     or use environment variables:
     export SL_LOCALE=**-**
     export SL_USER_IDENTIFIER=******************************
     export SL_USER_SECRET=*******************************************************
     
     #optional
     export SL_ACCOUNT_UID=******* #required only to list projects api call
     export SL_PROJECT_ID=******* #required for api calls `projects` and `project_details`
    """

    def __init__(self, id):
        self.id = id
        
    def __str__(self):
        return "Missing:" + self.id + self.noKeymessage


class Credentials:

    MY_PROJECT_ID = "CHANGE_ME"
    MY_ACCOUNT_UID = "CHANGE_ME"
    MY_USER_IDENTIFIER = "CHANGE_ME"
    MY_USER_SECRET = "CHANGE_ME"
    MY_LOCALE="CHANGE_ME"
    
    creds = ("PROJECT_ID", "ACCOUNT_UID", "USER_IDENTIFIER", "USER_SECRET", "LOCALE")
    optional_creds = ("ACCOUNT_UID")
   
    def __init__(self):
        for id in self.creds:
            cred = "MY_"+id
            value = getattr(self, cred, "CHANGE_ME")
            if "CHANGE_ME" == value:
                value = os.environ.get('SL_'+id, getattr(self, cred))    
            if "CHANGE_ME" == value and not id in self.optional_creds:
                raise CredentialsNotSet(id)
            setattr(self, cred, value)
