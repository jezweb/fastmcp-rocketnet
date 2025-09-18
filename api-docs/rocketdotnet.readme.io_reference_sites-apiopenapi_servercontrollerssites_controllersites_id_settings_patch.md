---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollerssites_controllersites_id_settings_patch"
title: "Update site settings."
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Retrieving recent requests… |

LoadingLoading…

#### URL Expired

The URL for this request expired after 30 days.

id

integer

required

ID of the Site you are interacting with

Site's Settings

new\_php\_version

string

enum

new php version for the site to use

5.67.07.27.37.48.08.18.28.3

Show 9 enum values

wp\_admin\_sso\_default\_user\_id

integer

≥ 1

The ID of the default wp-admin SSO user

wp\_core\_auto\_updates

integer

enum

Control WordPress Core Auto-Updates: 0 - No auto-updates, 1 - Update all versions, 2 - Update minor/patch versions only

012

Allowed:

`0``1``2`

wp\_theme\_auto\_updates

integer

enum

01

Allowed:

`0``1`

wp\_plugin\_auto\_updates

integer

enum

01

Allowed:

`0``1`

ssh\_access

integer

enum

01

Allowed:

`0``1`

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

2     --url https://api.rocket.net/v1/sites/id/settings \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *