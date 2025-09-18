---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersreporting_controllerreporting_sites_id_waf_eventlist_get"
title: "List WAF Events"
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

duration

string

enum

required

Duration that the listed data is for (m = minutes, h = hours, d = days)

30m1h6h12h24h72h7d30d

Show 8 enum values

search

string

Search for an event by action, client\_ip, country, request\_path, user\_agent, or query\_string

action

array of strings

Filter events matching a specific action taken by the WAF

action
ADD string

client\_ip

string

Filter events matching a specific IP address

request\_path

string

Filter events matching a specific request path or partial path

country

array of strings

Filter events matching a specific country

country
ADD string

asn

string

Filter events matching a specific ASN

asn\_description

string

Filter events matching a specific or partial ASN description

http\_method

array of strings

Filter events matching a specific HTTP method

http\_method
ADD string

http\_protocol

string

Filter events matching a specific or partial HTTP Protocol

query\_string

string

Filter events matching a specific or partial Query String

ray\_id

string

Filter events matching a specific or partial Ray ID

user\_agent

string

Filter events matching a specific or partial HTTP User Agent

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

2     --url 'https://api.rocket.net/v1/reporting/sites/id/waf/eventlist?duration=30m&per_page=10&page=1' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *