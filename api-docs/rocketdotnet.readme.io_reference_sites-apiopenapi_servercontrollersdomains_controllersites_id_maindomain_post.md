---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersdomains_controllersites_id_maindomain_post"
title: "Set a domain for a Site"
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

Initial main domain information.

domain

string

Site's domain name

keep\_cdn\_url

boolean

Defaults to false

When set, DNS records for the live domain will be returned but the WordPress install will stay on the CDN URL (WordPress can only have one domain). This is useful for testing the site before going live while setting TXT records for SSL and Hostname validation

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

1curl --request POST \

2     --url https://api.rocket.net/v1/sites/id/maindomain \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json' \

5     --data '

6{

7  "keep_cdn_url": false

8}

9'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *