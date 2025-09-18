---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersplugins_controllersites_id_plugins_post"
title: "Install new WordPress plugins to site"
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

plugins

string

Comma separated list of plugins to install. Cannot be combined with 'custom\_url'

activate

boolean

Defaults to false

If all the plugins that are being installed should be activated

truefalse

custom\_url

string

If a plugin should be downloaded from a custom URL rather than the wordpress.org plugin library, this is the download URL. Cannot be combined with 'plugins'

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

2     --url https://api.rocket.net/v1/sites/id/plugins \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json' \

5     --data '{"activate":false}'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *