---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersdomains_controllersites_id_maindomain_patch"
title: "Update maindomain validation method or SSL CA"
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

Updated validation method.

domain

string

Domain name to update should you wish to change the maindomain that is not the primary maindomain

validation\_method

string

enum

Validation method to use (http = http, txt = DNS)

httptxt

Allowed:

`http``txt`

hide\_go\_live

integer

enum

Hide the Go Live information in the UI now that Go Live is complete

01

Allowed:

`0``1`

certificate\_authority

string

enum

Certificate Authority to be used to issue SSL certificates for the site

googlelets\_encrypt

Allowed:

`google``lets_encrypt`

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

2     --url https://api.rocket.net/v1/sites/id/maindomain \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *