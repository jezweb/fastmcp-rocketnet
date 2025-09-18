---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersreporting_controllersites_id_reporting_cdn_request_volume_by_source_get"
title: "CDN Request Volume by Source"
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

duration

string

enum

required

Duration that the listed data is for (m = minutes, h = hours, d = days)

30m1h6h12h24h72h7d30d

Show 8 enum values

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

1curl --request GET \

2     --url 'https://api.rocket.net/v1/sites/id/reporting/cdn_request_volume_by_source?duration=30m' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *