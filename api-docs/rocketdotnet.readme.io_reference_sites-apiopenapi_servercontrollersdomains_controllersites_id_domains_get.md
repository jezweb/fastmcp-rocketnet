---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersdomains_controllersites_id_domains_get"
title: "List additional domains (aliases) for the site"
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

search

string

Search for a domain by its name

page

integer

Defaults to 1

Page of results to include

per\_page

integer

Defaults to 100

How many results to include in each page

sort

string

enum

property to sort the results by

domaindomain\_typehostname\_statusssl\_statusvalidation\_method

Allowed:

`domain``domain_type``hostname_status``ssl_status``validation_method`

direction

string

enum

Direction to sort results in (asc = ascending, desc = descending)

ascdescASCDESC

Allowed:

`asc``desc``ASC``DESC`

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

2     --url 'https://api.rocket.net/v1/sites/id/domains?page=1&per_page=100' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *