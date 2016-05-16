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

from setuptools import setup

setup(
    name="SmartlingApiSdk",
    version = "2.0.2",
    author="Smartling, Inc.",
    author_email="aartamonov@smartling.com",
    description="Smartling python library for file translations",
    license='Apache License v2.0',
    keywords='translation localization internationalization',
    url="https://docs.smartling.com/display/docs/Files+API",
    long_description="python SDK to work with Smartling API for file translation",
    packages=['smartlingApiSdk', "simplejson24", "example", "test"],
    include_package_data = True,
    package_data = {
        '': ['*.properties', '*.xml'],
    },
   
)
