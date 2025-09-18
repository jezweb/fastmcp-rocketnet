---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersbilling_controllerpatch_billing_payment_methods_method_id"
title: "Update Payment Method"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Retrieving recent requests… |

LoadingLoading…

#### URL Expired

The URL for this request expired after 30 days.

payment\_method\_id

integer

required

Create a Payment Method

active

boolean

Use this payment method for all automated payments

truefalse

address\_id

integer

ID of the billing address used for this payment method

description

string

Optional description of the card

expiry\_date

string

length between 5 and 5

Expiration month and year of the payment method (if it is a credit card)

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

1curl --request PATCH \

2     --url https://api.rocket.net/v1/billing/payment_methods/payment_method_id \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 405`` 500

Updated 4 months ago

* * *