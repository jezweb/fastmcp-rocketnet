---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersthemes_controllersites_id_themes_search_get"
title: "Search for WordPress themes that can be installed"
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

query

string

Search terms

page

integer

≥ 1

Defaults to 1

Page of results to include (default = 1)

per\_page

integer

1 to 1000

Defaults to 10

How many results to include in each page (default = 10)

browse

string

enum

response ordering. Leave off for default order

featurednewpopularupdated

Allowed:

`featured``new``popular``updated`

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

2     --url 'https://api.rocket.net/v1/sites/id/themes/search?page=1&per_page=10' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *