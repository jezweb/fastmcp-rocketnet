---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersftp_accounts_controllersites_id_ftp_accounts_patch"
title: "Update ftp account"
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

username

string

required

FTP account username (with domain)

Updated ftp account parameters

new\_password

string

Password for the FTP account

quota

integer

Defaults to 0

FTP disk space quota in MB (0 = unlimited)

homedir

string

Document root for the FTP account (relative the user's home directory)

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

1curl --request PATCH \

2     --url https://api.rocket.net/v1/sites/id/ftp/accounts \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json' \

5     --data '{"quota":0}'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *