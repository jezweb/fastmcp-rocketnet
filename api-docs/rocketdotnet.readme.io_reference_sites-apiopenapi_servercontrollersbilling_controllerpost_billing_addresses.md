---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersbilling_controllerpost_billing_addresses"
title: "Create Billing Address"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Make a request to see history. |

#### URL Expired

The URL for this request expired after 30 days.

Create a new billing address

first\_name

string

required

First name of the billing contact

last\_name

string

required

Last name of the billing contact

address\_line\_1

string

required

First Address line of the billing contact

address\_line\_2

string

Second Address line of the billing contact

company\_name

string

Company name of the billing contact

email

string

required

Email address of the billing contact

city

string

required

City of the billing contact

state

string

required

State / Province of the billing contact

country

string

required

Country Code of the billing contact

postal\_code

string

required

Postal code of the billing contact

telephone

string

required

Telephone number of the billing contact

receive\_invoice\_emails

boolean

Defaults to false

Setting to true will CC this email address on invoice emails

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

1curl --request POST \

2     --url https://api.rocket.net/v1/billing/addresses \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json' \

5     --data '

6{

7  "receive_invoice_emails": false

8}

9'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 405`` 500

Updated 4 months ago

* * *