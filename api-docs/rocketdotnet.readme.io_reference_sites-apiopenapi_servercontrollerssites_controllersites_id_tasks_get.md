---
url: "https://rocketdotnet.readme.io/reference/sites-apiopenapi_servercontrollerssites_controllersites_id_tasks_get"
title: "List Site Tasks"
---

| time | status | user agent |  |
| :-- | :-- | :-- | :-- |
| Make a request to see history. |

#### URL Expired

The URL for this request expired after 30 days.

id

integer

required

ID of the Site you are interacting with

task\_id

uuid

ID of this task

task\_type

string

enum

Type of task

automated\_restorebackupclone\_sitecloud\_backup\_createcloud\_backup\_restorepublishrestorestaging

Show 8 enum values

task\_status

string

enum

Current state/status of the task

DONEERRORNEWPROGRESS

Allowed:

`DONE``ERROR``NEW``PROGRESS`

page

integer

≥ 1

Defaults to 1

Page of results to include (default = 1)

per\_page

integer

Defaults to 100

Results per page

sort

string

enum

idperctask\_statustask\_typeupdated

Allowed:

`id``perc``task_status``task_type``updated`

direction

string

enum

Direction to sort results in (asc = ascending, desc = descending)

ascdescASCDESC

Allowed:

`asc``desc``ASC``DESC`

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

1curl --request GET \

2     --url 'https://api.rocket.net/v1/sites/id/tasks?page=1&per_page=100' \

3     --header 'accept: application/json'

```

Click `Try It!` to start a request and see the response here! Or choose an example:

application/json

`` 200`` 400`` 401`` 403`` 404`` 405`` 500

Updated 4 months ago

* * *