---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersbilling_controllerpatch_billing_invoices_invoice_id_paypal_subscription"
title: "Update a PayPal Subscription"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Make a request to see history. |

#### URL Expired

The URL for this request expired after 30 days.

invoice\_id

integer

required

Record a subscription creation

paypal\_order\_id

string

required

ID of the order that is returned from PayPal SDK onApprove

paypal\_subscription\_id

string

required

ID of the subscription that is returned from PayPal SDK onApprove

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

1curl --request PATCH \

2     --url https://api.rocket.net/v1/billing/invoices/invoice_id/paypal_subscription \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 405`` 412`` 500

Updated 4 months ago

* * *