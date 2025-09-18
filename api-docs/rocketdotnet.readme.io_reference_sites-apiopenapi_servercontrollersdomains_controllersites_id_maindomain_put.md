---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersdomains_controllersites_id_maindomain_put"
title: "Replace current maindomain with different one"
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

New maindomain.

domain

string

Site's new domain name

active\_wordpress\_domain

string

enum

Switch between the Live domain name and CDN URL. WARNING: WordPress can only have 1 URL and this will break your live site if you switch to CDN URL

cdn\_urllive\_domain

Allowed:

`cdn_url``live_domain`

remove\_live\_domain

boolean

Defaults to false

Use this in conjunction with `active_wordpress_domain` set to `cdn_url` to revert this site back to a cdn\_url from live domain. Warning: This will cause the live domain to no longer function and will remove all additional domains

truefalse

convert\_addon\_to\_maindomain

boolean

Defaults to false

Use this to convert an addon domain to the maindomain. The `domain` passed will be converted from an addon domain to the maindomain and the existing maindomain will be removed.

truefalse

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

10

1curl --request PUT \

2     --url https://api.rocket.net/v1/sites/id/maindomain \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json' \

5     --data '

6{

7  "remove_live_domain": false,

8  "convert_addon_to_maindomain": false

9}

10'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *