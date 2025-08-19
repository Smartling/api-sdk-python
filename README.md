# Smartling Python API SDK

This repository contains the official Python SDK for interacting with the Smartling Translation APIs.

Smartling provides a cloud-based software and translation services solution that automates content translation and integration. This SDK allows developers to seamlessly internationalize their websites and applications by automating the translation and integration of content. You can upload resource files and download translated files in various locales, utilizing professional, community, or machine translation options.

For a full description of the Smartling APIs, please refer to the [Smartling API Reference](https://api-reference.smartling.com/).

This SDK covers the following Smartling APIs:
*   Jobs
*   Job Batches V2
*   Strings
*   Context
*   Estimates
*   Account & Projects
*   Files
*   Tags

## Table of Contents
*   [Installation](#installation)
*   [Quick Start](#quick-start)
*   [Examples](#examples)
*   [Testing](#testing)
*   [Versioning](#versioning)
*   [Bug Tracker](#bug-tracker)
*   [Authors](#authors)
*   [Copyright and License](#copyright-and-license)

## Installation

It is recommended to use a virtual environment for development:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[test]
```

## Quick Start

The Smartling API v2 is the recommended version for all new integrations. The API v1 is deprecated and should only be used for maintaining existing integrations.

To get started with API v2, you'll need your User Identifier and User Secret. You can find these in your Smartling account settings.

Here's a basic example using the Files API v2:

```python
import os
from smartlingApiSdk.ApiV2 import ApiV2
from smartlingApiSdk.UploadData import UploadData
from smartlingApiSdk.Constants import FileTypes

# Set your Smartling API credentials as environment variables
# export SL_USER_IDENTIFIER="your_user_identifier"
# export SL_USER_SECRET="your_user_secret"
# export SL_PROJECT_ID="your_project_id"

user_identifier = os.environ.get('SL_USER_IDENTIFIER')
user_secret = os.environ.get('SL_USER_SECRET')
project_id = os.environ.get('SL_PROJECT_ID')

if not all([user_identifier, user_secret, project_id]):
    print("Please set SL_USER_IDENTIFIER, SL_USER_SECRET, and SL_PROJECT_ID environment variables.")
else:
    try:
        api = ApiV2(user_identifier, user_secret, project_id)

        # Example: Upload a file
        file_path = "path/to/your/file.xml" # Replace with your file path
        file_uri = "my_example_file.xml"
        file_type = FileTypes.xml

        upload_data = UploadData(file_path, file_uri, file_type)
        response, status_code = api.upload(upload_data)

        if status_code == 200:
            print(f"File uploaded successfully: {response.data.fileUri}")
        else:
            print(f"File upload failed: {response.code} - {response.messages}")

    except Exception as e:
        print(f"An error occurred: {e}")
```

## Examples

More extensive examples covering almost every API call are available in the `smartlingApiSdk/example` directory.

You can run them as follows:

```python
from smartlingApiSdk.example.StringsExample import example
example()

# Or try other examples:
# from smartlingApiSdk.example.FilesSimpleExample import example
# from smartlingApiSdk.example.FilesExample import example
# from smartlingApiSdk.example.AccountProjectsExample import example
# from smartlingApiSdk.example.ContextExample import example
# from smartlingApiSdk.example.EstimatesExample import example
# from smartlingApiSdk.example.JobsExample import example
# from smartlingApiSdk.example.JobBatchesV2Example import example
# from smartlingApiSdk.example.TagsExample import example
# from smartlingApiSdk.example.MultipleAccountsExample import example
# from smartlingApiSdk.example.MultipleProjectsExample import example
```

## Testing

This project uses `pytest` for testing.

To run the tests, first ensure you have installed the test dependencies:

```bash
pip install -e .[test]
```

Then, execute `pytest` from the project root:

```bash
/Users/kvac/workspace/projects/api-sdk-python/.venv/bin/pytest
```

**Note:** Some tests require valid Smartling API credentials. Please set the following environment variables:
*   `SL_API_KEY`
*   `SL_PROJECT_ID`
*   `SL_USER_IDENTIFIER`
*   `SL_USER_SECRET`
*   `SL_LOCALE` (for locale-specific tests)

## Versioning

For transparency and insight into our release cycle, and for striving to maintain backward compatibility, the File Translation API SDK will be maintained under the Semantic Versioning guidelines as much as possible.

Releases will be numbered with the following format:

`<major>.<minor>.<patch>`

And constructed with the following guidelines:

*   Breaking backward compatibility bumps the major
*   New additions without breaking backward compatibility bumps the minor
*   Bug fixes and miscellaneous changes bump the patch

For more information on SemVer, please visit [http://semver.org/](http://semver.org/).

## Bug Tracker

Have a bug? Please create an issue here on GitHub: [https://github.com/Smartling/api-sdk-python/issues](https://github.com/Smartling/api-sdk-python/issues)

## Authors

*   **Anatoly Artamonov**
    *   [GitHub](https://github.com/anatolija)
    *   aartamonov@smartling.com
*   **Alex Koval**
    *   [GitHub](https://github.com/junky)
    *   akoval@smartling.com
*   **Greg Jones**
    *   [GitHub](http://github.com/jones-smartling)
    *   gjones@smartling.com

## Copyright and License

Copyright 2012-2025 Smartling, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this work except in compliance with the License.
You may obtain a copy of the License in the LICENSE file, or at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.