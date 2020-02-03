[Smartling File Translation API](https://developer.smartling.com/docs/sdks-2)
=================

This repository contains the Python SDK for accessing the Smartling Translation API.

Smartling is cloud-based software and translation services solution prioritizes process automation and intelligent collaboration.
The Smartling File Translation API allows developers to seamlessly internationalize their website 
or application by automating the translation and integration of content.
Developers can upload resource files and download the translated file(s) in a locale of their choosing.
There are options allowing to use professional translation, community translation or machine translation.

For a full description of the Smartling File Translation API, please read File API section of the docs at: https://developer.smartling.com/docs/sdks-2 


Quick start
-----------

Clone the repo: `git clone git@github.com:Smartling/api-sdk-python.git`.
You may start with examples in ./example directory.
There are 4 examples:

SimpleExample.py - contains basic file API SDK operartions

IntermediateExample.py - introduces a bit more advanced file API example: rename, import and SmartlingDirectives

AdvancedExample.py - calls every file API call and tests response values

ProjectsExample.py - calls projects API and tests response values


Versioning
----------

For transparency and insight into our release cycle, and for striving to maintain backward compatibility, the File Translation API SDK will be maintained under the Semantic Versioning guidelines as much as possible.

Releases will be numbered with the follow format:

`<major>.<minor>.<patch>`

And constructed with the following guidelines:

* Breaking backward compatibility bumps the major
* New additions without breaking backward compatibility bumps the minor
* Bug fixes and misc changes bump the patch

For more information on SemVer, please visit http://semver.org/.


Bug tracker
-----------

Have a bug? Please create an issue here on GitHub!

https://github.com/Smartling/api-sdk-python/issues


Authors
-------

Anatoly Artamonov
* https://github.com/anatolija
* aartamonov@smartling.com

Alex Koval
* https://github.com/junky
* akoval@smartling.com

Greg Jones
* http://github.com/jones-smartling
* gjones@smartling.com


Copyright and license
---------------------

Copyright 2012-2018 Smartling, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this work except in compliance with the License.
You may obtain a copy of the License in the LICENSE file, or at:

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
