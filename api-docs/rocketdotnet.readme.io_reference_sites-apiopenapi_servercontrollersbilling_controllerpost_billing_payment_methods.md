---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersbilling_controllerpost_billing_payment_methods"
title: "Add Credit Card"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Retrieving recent requests… |

LoadingLoading…

#### URL Expired

The URL for this request expired after 30 days.

Credit Card information

active

boolean

Defaults to false

Use this payment method for all automated payments

truefalse

card\_token

string

required

Tokenized Credit Card string

description

string

Optional description of the card

address\_id

integer

required

ID of the billing address used for this payment method

# `` 200      OK

# `` 400      Bad Request

# `` 401      Authentication failed

# `` 403      Not authorized to access endpoint

# `` 405      Invalid input

# `` 500      Internal error

Updated 4 months ago

* * *

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request POST \

2     --url https://api.rocket.net/v1/billing/payment_methods \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json' \

5     --data '{"active":false}'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 405`` 500

Updated 4 months ago

* * *