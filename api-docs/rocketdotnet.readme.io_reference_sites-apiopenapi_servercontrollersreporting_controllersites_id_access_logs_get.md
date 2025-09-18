---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersreporting_controllersites_id_access_logs_get"
title: "List Access Logs"
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

domain

string

required

Domain that received the request

ip

string

IP address related to the request

cache\_status

string

enum

Type of cache interaction

bypassdynamicexpiredhitmissnonestable

Allowed:

`bypass``dynamic``expired``hit``miss``none``stable`

uri

string

URI being requested

ray\_id

string

Unique Request ID

device\_type

string

enum

Device Type

desktopmobiletablet

Allowed:

`desktop``mobile``tablet`

status\_code

string

HTTP Status Code of the Request

per\_page

integer

1 to 1000

Defaults to 10

How many results to include in each page (default = 10)

page

integer

≥ 1

Defaults to 1

Page of results to include (default = 1)

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

2     --url 'https://api.rocket.net/v1/sites/id/access_logs?duration=30m&per_page=10&page=1' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *