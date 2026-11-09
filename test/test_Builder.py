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

lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from builder.Method import Method, UnsupportedSchema
from builder.ApiSource import ApiSource
from nose.tools import assert_equal, assert_raises

SWAGGER = {
    'components': {
        'parameters': {
            'projectUid': {'name': 'projectUid', 'in': 'path', 'required': True, 'schema': {'type': 'string'}},
            'offset': {'name': 'offset', 'in': 'query', 'schema': {'type': 'integer', 'default': 0}},
        },
        'schemas': {
            'A': {'type': 'object', 'properties': {'kind': {'type': 'string'}}},
            'B': {'type': 'object', 'properties': {'kind': {'type': 'string'}}},
        },
    },
}


def operation(operationId='op', parameters=None, requestBody=None):
    descr = {'operationId': operationId, 'tags': ['Test'], 'parameters': parameters or []}
    if requestBody:
        descr['requestBody'] = requestBody
    return descr


class test_Builder(object):

    def test_ref_projectUid_becomes_projectId_member(self):
        descr = operation(parameters=[{'$ref': '#/components/parameters/projectUid'},
                                      {'$ref': '#/components/parameters/offset'}])
        m = Method('Test', 'test', '/x-api/v2/projects/{projectUid}/items', 'get', descr, SWAGGER)

        assert_equal(m.path, '/x-api/v2/projects/{projectId}/items')
        assert_equal([p._name for p in m.parameters], ['offset'])

    def test_inline_projectUid_stays_explicit_parameter(self):
        descr = operation(parameters=[{'name': 'projectUid', 'in': 'path', 'required': True, 'schema': {'type': 'string'}}])
        m = Method('Test', 'test', '/x-api/v2/projects/{projectUid}/items', 'get', descr, SWAGGER)

        assert_equal(m.path, '/x-api/v2/projects/{projectUid}/items')
        assert_equal([p._name for p in m.parameters], ['projectUid'])

    def test_oneOf_body_raises_unsupported(self):
        body = {'content': {'application/json': {'schema': {'oneOf': [{'$ref': '#/components/schemas/A'},
                                                                      {'$ref': '#/components/schemas/B'}]}}}}
        descr = operation(requestBody=body)
        assert_raises(UnsupportedSchema, Method, 'Test', 'test', '/x', 'post', descr, SWAGGER)

    def test_collect_skips_unsupported_and_duplicate_operations(self):
        oneOf = {'content': {'application/json': {'schema': {'oneOf': [{'$ref': '#/components/schemas/A'}]}}}}
        swagger = dict(SWAGGER)
        swagger['paths'] = {
            '/ok': {'get': operation('okOperation')},
            '/one-of': {'post': operation('oneOfOperation', requestBody=oneOf)},
            '/dup': {'post': operation('getAllSourceStringsByProjectPost')},
        }
        src = ApiSource('Test', 'Test')
        src.collectMethods(swagger)

        assert_equal([m.operationId for m in src.methods], ['okOperation'])
