#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012-2025 Smartling, Inc.
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
import sys
import json

lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from smartlingApiSdk.AuthClient import AuthClient
from nose.tools import assert_equal

AUTH_URI = AuthClient.authUri
REFRESH_URI = AuthClient.refreshUri
ACCESS_TTL = 480
REFRESH_TTL = 3660


def authResponse(accessToken, refreshExpiresIn=REFRESH_TTL, expiresIn=ACCESS_TTL):
    data = {'accessToken': accessToken, 'refreshToken': 'refresh-' + accessToken,
            'expiresIn': expiresIn, 'refreshExpiresIn': refreshExpiresIn, 'tokenType': 'Bearer'}
    return json.dumps({'response': {'code': 'SUCCESS', 'data': data}}).encode(), 200, {}


ERROR_RESPONSE = (json.dumps({'response': {'code': 'AUTHENTICATION_ERROR', 'errors': []}}).encode(), 401, {})


class test_AuthClient(object):

    def setUp(self):
        self.client = AuthClient('host', 'userIdentifier', 'userSecret')
        self.client.httpClient.getHttpResponseAndStatus = self.mock_response
        self.calls = []
        self.responses = {}

    def mock_response(self, method, uri, params, extraHeaders=None, requestBody=None):
        self.calls.append(uri)
        return self.responses[uri].pop(0)

    def respond(self, uri, *responses):
        self.responses.setdefault(uri, []).extend(responses)

    def authenticateInitially(self):
        self.respond(AUTH_URI, authResponse('initial'))
        assert_equal(self.client.getToken(), 'initial')
        self.calls = []
        self.client.accessExpiresAt = 0  # access token expired, refresh token still valid

    def test_initial_authentication(self):
        self.respond(AUTH_URI, authResponse('initial'))

        assert_equal(self.client.getToken(), 'initial')
        assert_equal(self.client.getToken(), 'initial')  # cached, no new request
        assert_equal(self.calls, [AUTH_URI])
        assert_equal(self.client.refreshToken, 'refresh-initial')

    def test_smartling_user_authenticates_via_user_endpoint(self):
        self.client.userIdentifier = 'someone@smartling.com'
        self.respond(AUTH_URI + '/user', authResponse('user'))

        assert_equal(self.client.getToken(), 'user')
        assert_equal(self.calls, [AUTH_URI + '/user'])

    def test_normal_refresh(self):
        self.authenticateInitially()
        self.respond(REFRESH_URI, authResponse('refreshed'))

        assert_equal(self.client.getToken(), 'refreshed')
        assert_equal(self.calls, [REFRESH_URI])

    def test_session_capped_refresh_reauthenticates(self):
        self.authenticateInitially()
        self.respond(REFRESH_URI, authResponse('capped', refreshExpiresIn=45, expiresIn=45))
        self.respond(AUTH_URI, authResponse('new-session'))

        assert_equal(self.client.getToken(), 'new-session')
        assert_equal(self.calls, [REFRESH_URI, AUTH_URI])
        assert_equal(self.client.refreshToken, 'refresh-new-session')

    def test_refresh_at_threshold_is_not_session_capped(self):
        self.authenticateInitially()
        self.respond(REFRESH_URI, authResponse('refreshed', refreshExpiresIn=AuthClient.sessionCapThreshold))

        assert_equal(self.client.getToken(), 'refreshed')
        assert_equal(self.calls, [REFRESH_URI])

    def test_failed_refresh_reauthenticates(self):
        self.authenticateInitially()
        self.respond(REFRESH_URI, ERROR_RESPONSE)
        self.respond(AUTH_URI, authResponse('new-session'))

        assert_equal(self.client.getToken(), 'new-session')
        assert_equal(self.calls, [REFRESH_URI, AUTH_URI])

    def test_expired_refresh_token_authenticates(self):
        self.authenticateInitially()
        self.client.refreshExpiresAt = 0
        self.respond(AUTH_URI, authResponse('new-session'))

        assert_equal(self.client.getToken(), 'new-session')
        assert_equal(self.calls, [AUTH_URI])
