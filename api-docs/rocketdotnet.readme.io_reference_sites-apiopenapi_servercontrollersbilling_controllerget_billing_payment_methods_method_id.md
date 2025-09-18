---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersbilling_controllerget_billing_payment_methods_method_id"
title: "Get Payment Method"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Make a request to see history. |

#### URL Expired

The URL for this request expired after 30 days.

payment\_method\_id

integer

required

include\_token

boolean

Defaults to false

Include the token used at the payment gateway in the response

truefalse

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

1curl --request GET \

2     --url 'https://api.rocket.net/v1/billing/payment_methods/payment_method_id?include_token=false' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 405`` 500

Updated 4 months ago

* * *