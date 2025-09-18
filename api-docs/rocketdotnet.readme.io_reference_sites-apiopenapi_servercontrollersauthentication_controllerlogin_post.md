---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersauthentication_controllerlogin_post"
title: "Authenticate user and generate JWT token"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Make a request to see history. |

#### URL Expired

The URL for this request expired after 30 days.

Username and password to authenticate user

username

string

required

Username to use for authentication

password

string

required

Password to use for authentication

# `` 200      OK

# `` 400      Invalid or missing request parameters

# `` 401      Authentication failed

# `` 500      Unable to authenticate

Updated 4 months ago

* * *

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request POST \

2     --url https://api.rocket.net/v1/login \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 500

Updated 4 months ago

* * *