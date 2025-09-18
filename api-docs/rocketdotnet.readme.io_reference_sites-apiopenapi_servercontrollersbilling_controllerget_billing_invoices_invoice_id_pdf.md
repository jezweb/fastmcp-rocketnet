---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersbilling_controllerget_billing_invoices_invoice_id_pdf"
title: "Download Invoice PDF"
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

token

string

required

embed

boolean

Defaults to false

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

2     --url 'https://api.rocket.net/v1/billing/invoices/invoice_id/pdf?embed=false' \

3     --header 'accept: application/pdf'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/pdf

`` 200

application/json

`` 400`` 401`` 403`` 405`` 500

Updated 4 months ago

* * *