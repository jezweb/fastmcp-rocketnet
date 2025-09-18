---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollerssites_controllersites_post"
title: "Create new site"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Make a request to see history. |

#### URL Expired

The URL for this request expired after 30 days.

New site parameters

name

string

required

WordPress Site Title

location

integer

Which Rocket.net Point of Presence to create the site at

restricted\_location

integer

If you have dedicated locations, you can use these by ID to add sites at those dedicated locations. (When passed, do not pass location)

admin\_username

string

WordPress admin user

admin\_password

string

WordPress admin password

admin\_email

string

WordPress admin email

multisite

boolean

Defaults to false

If the site will use WordPress Multisite: [https://wordpress.org/documentation/article/wordpress-glossary/#multisite](https://wordpress.org/documentation/article/wordpress-glossary/#multisite)

truefalse

template\_id

uuid

An optional Site Template ID to use when creating the site

install\_plugins

string

A comma separated list of plugin slugs to install

sub\_path

string

If the site should be installed outside of public\_html, which folder (this is rare)

label

string

Label for the site (can be used to look up sites)

static\_site

boolean

When true, a static site will be created without any WordPress install

truefalse

metadata

object

metadata object

php\_version

string

PHP version to be used

template\_replacements

array of objects

If this site is being created from a template, pass keys and values here and they will be replaced in the site's database

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

2     --url https://api.rocket.net/v1/sites \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json' \

5     --data '{"multisite":false}'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *