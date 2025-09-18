---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollerssite_templates_controllersites_templates_get"
title: "List Site Templates"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Make a request to see history. |

#### URL Expired

The URL for this request expired after 30 days.

created\_from.site\_id

integer

If passed, will restrict the response to results matching the site ID the template was created from

created\_from.domain

string

If passed, will restrict the response to results matching the domain the template was created from

tags

array of strings

If passed, will restrict the response to results matching these tags

tags
ADD string

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

sort

string

enum

Which property to sort the results by

namecreated\_atupdated\_at

Allowed:

`name``created_at``updated_at`

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

2     --url 'https://api.rocket.net/v1/sites/templates?page=1&per_page=10' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *