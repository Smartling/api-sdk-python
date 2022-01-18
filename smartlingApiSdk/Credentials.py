#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012-2021 Smartling, Inc.
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

import os


class CredentialsNotSet(Exception):
    noKeyMessage = """ 
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

    def __init__(self, id, env):
        self.id = id
        self.env = env

    def getMessage(self):
        res = self.noKeyMessage
        if 'stg' == self.env:
            res = res.replace('SL_USER_IDENTIFIER=', 'SL_USER_IDENTIFIER_STG=')
            res = res.replace('SL_USER_SECRET=', 'SL_USER_SECRET_STG=')
        return res

    def __str__(self):
        return "Missing:" + self.id + self.getMessage()


class Credentials():

    MY_PROJECT_ID = "CHANGE_ME"
    MY_ACCOUNT_UID = "CHANGE_ME"
    MY_USER_IDENTIFIER = "CHANGE_ME"
    MY_USER_SECRET = "CHANGE_ME"
    MY_LOCALE ="CHANGE_ME"

    CREDS = ("PROJECT_ID", "ACCOUNT_UID", "USER_IDENTIFIER", "USER_SECRET", "LOCALE")
    OPTIONAL_CREDS = ("ACCOUNT_UID", "LOCALE")
   
    def __init__(self, env='prod'):
        for id in self.CREDS:
            cred = "MY_"+id
            suffix = ''
            if env == 'stg' and id.startswith("USER_"):
                suffix = '_STG'
            value = getattr(self, cred + suffix, "CHANGE_ME")
            if "CHANGE_ME" == value:
                value = os.environ.get('SL_' + id + suffix, getattr(self, cred))
            if "CHANGE_ME" == value and id not in self.OPTIONAL_CREDS:
                raise CredentialsNotSet('SL_' + id + suffix, env)
            setattr(self, cred, value)
