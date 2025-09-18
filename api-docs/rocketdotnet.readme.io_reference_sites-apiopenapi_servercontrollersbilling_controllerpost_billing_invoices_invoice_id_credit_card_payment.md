---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersbilling_controllerpost_billing_invoices_invoice_id_credit_card_payment"
title: "Record a Credit Card Payment"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Retrieving recent requests… |

LoadingLoading…

#### URL Expired

The URL for this request expired after 30 days.

invoice\_id

integer

required

Record a gateway payment

gateway\_token

string

required

Gateway token that is being charged

payment\_method\_id

integer

required

ID of the payment method being used

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

1curl --request POST \

2     --url https://api.rocket.net/v1/billing/invoices/invoice_id/credit_card_payment \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 405`` 412`` 500

Updated 4 months ago

* * *