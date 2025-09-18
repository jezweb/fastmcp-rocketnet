---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollerscdn_cache_controllersites_id_cache_purge_post"
title: "Purge files from cache on cloudflare"
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

staging

boolean

truefalse

domain

string

include\_additional\_domains

boolean

Defaults to false

Also purge any additional domains for the site

truefalse

Purge cache list of files

files

array of strings

files
ADD string

tags

array of strings

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

2     --url 'https://api.rocket.net/v1/sites/id/cache/purge?include_additional_domains=false' \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *