---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollersdomains_controllersites_id_maindomain_edge_settings_patch"
title: "Update Maindomain Edge Settings"
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

Updated MaindomainEdge Settings

ai\_crawlers

object

EdgeSettingsAICrawlers object

logged\_in\_users

object

EdgeSettingsLoggedInUsers object

managed\_challenge

object

EdgeSettingsManagedChallenge object

user\_agent

object

EdgeSettingsUserAgent object

woocommerce

object

EdgeSettingsWooCommerce object

wp\_login

object

EdgeSettingsWPLogin object

xmlrpc\_protection

object

EdgeSettingsXMLRPCProtection object

# `` 200      OK

# `` 400      Bad Request

# `` 401      Authentication failed

# `` 403      Not authorized to access endpoint

# `` 404      Given site not found for user

# `` 405      Invalid input

# `` 500      Internal error

Updated 2 months ago

* * *

ShellNodeRubyPHPPython

```

xxxxxxxxxx

40

1curl --request PATCH \

2     --url https://api.rocket.net/v1/sites/id/maindomain/edge_settings \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json' \

5     --data '

6{

7  "ai_crawlers": {

8    "allow": null

9  },

10  "logged_in_users": {

11    "waf_bypass": {

12      "enabled": null

13    }

14  },

15  "managed_challenge": {

16    "enabled": null

17  },

18  "user_agent": {

19    "empty": {

20      "allow": null

21    },

22    "go_http_client": {

23      "allow": null

24    }

25  },

26  "woocommerce": {

27    "login_and_registration_protection": {

28      "enabled": null

29    }

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 2 months ago

* * *