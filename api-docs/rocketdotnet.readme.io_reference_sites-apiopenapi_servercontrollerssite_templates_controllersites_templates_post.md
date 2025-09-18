---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollerssite_templates_controllersites_templates_post"
title: "[Deprecated]: Create new site template"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Retrieving recent requests… |

LoadingLoading…

#### URL Expired

The URL for this request expired after 30 days.

New site template parameters

name

string

required

length between 1 and 255

Name of the site template

site\_id

integer

required

Site ID to build the template from

notes

string

length ≥ 1

Notes about the site template

tags

array of strings

Tags which can be used identify templates

tags
ADD string

# `` 200      OK

# `` 400      Bad Request

# `` 401      Authentication failed

# `` 403      Not authorized to access endpoint

# `` 404      Given site not found for user

# `` 405      Invalid input

# `` 500      Internal error

Updated 4 months ago

* * *

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request POST \

2     --url https://api.rocket.net/v1/sites/templates \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *