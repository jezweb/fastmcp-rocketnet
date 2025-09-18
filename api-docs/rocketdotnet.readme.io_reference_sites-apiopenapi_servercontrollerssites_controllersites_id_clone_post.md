---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollerssites_controllersites_id_clone_post"
title: "Clone a site (via background task)"
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

New site parameters

location

integer

Which Rocket.net Point of Presence the cloned site should be created at

restricted\_location

integer

If you have dedicated locations, you can use these by ID to add sites at those dedicated locations. (When passed, do not pass location)

label

string

Label for the cloned site

metadata

object

metadata to add to the created site

metadata object

template\_replacements

array of objects

Pass keys and values here and they will be replaced in the site's database

template\_replacements
ADD object

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

1curl --request POST \

2     --url https://api.rocket.net/v1/sites/id/clone \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *