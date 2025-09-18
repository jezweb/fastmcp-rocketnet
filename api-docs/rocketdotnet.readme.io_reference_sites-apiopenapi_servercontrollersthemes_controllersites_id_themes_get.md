---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersthemes_controllersites_id_themes_get"
title: "List installed Wordpress themes on account"
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

Search theme name/title/description

page

integer

≥ 1

Defaults to 1

Page of results to include (default = 1)

per\_page

integer

Defaults to 50

Number of results per page

sort

string

enum

sort results by this property

descriptionnamestatustitleupdateversion

Allowed:

`description``name``status``title``update``version`

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

2     --url 'https://api.rocket.net/v1/sites/id/themes?page=1&per_page=50' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *