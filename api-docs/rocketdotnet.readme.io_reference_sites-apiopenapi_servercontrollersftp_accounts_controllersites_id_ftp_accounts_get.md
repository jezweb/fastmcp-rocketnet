---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersftp_accounts_controllersites_id_ftp_accounts_get"
title: "List Ftp Accounts"
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

username

string

Search for usernames matching this string

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

sort results by this property (omit for sort by user)

dirdiskquotadiskusedreldiruser

Allowed:

`dir``diskquota``diskused``reldir``user`

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

2     --url 'https://api.rocket.net/v1/sites/id/ftp/accounts?page=1&per_page=10' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *