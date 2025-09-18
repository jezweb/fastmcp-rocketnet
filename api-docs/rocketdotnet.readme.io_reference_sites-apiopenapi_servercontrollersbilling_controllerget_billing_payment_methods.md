---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersbilling_controllerget_billing_payment_methods"
title: "List Payment Methods"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Make a request to see history. |

#### URL Expired

The URL for this request expired after 30 days.

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

include\_token

boolean

Defaults to false

Include the token used at the payment gateway in the response

truefalse

active

boolean

Defaults to false

Include only an active payment method

truefalse

# `` 200      OK

# `` 400      Bad Request

# `` 401      Authentication failed

# `` 403      Not authorized to access endpoint

# `` 405      Invalid input

# `` 412      Precondition failed

# `` 500      Internal error

Updated 4 months ago

* * *

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url 'https://api.rocket.net/v1/billing/payment_methods?page=1&per_page=10&include_token=false&active=false' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 405`` 412`` 500

Updated 4 months ago

* * *