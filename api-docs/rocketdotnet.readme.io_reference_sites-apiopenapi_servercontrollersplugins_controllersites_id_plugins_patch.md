---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersplugins_controllersites_id_plugins_patch"
title: "Activate or deactivate WordPress plugins on given site"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Make a request to see history. |

#### URL Expired

The URL for this request expired after 30 days.

id

integer

required

ID of the Site you are interacting with

Plugin to be activated or deactivated

plugin

string

required

Plugin name/slug

status

string

enum

required

Activate or Deactivate a Plugin

activatedeactivate

Allowed:

`activate``deactivate`

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

1curl --request PATCH \

2     --url https://api.rocket.net/v1/sites/id/plugins \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json' \

5     --data '

6{

7  "status": "activate"

8}

9'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *