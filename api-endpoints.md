Here is a comprehensive list of all the API endpoints available for the Rocket.net API, categorized for your convenience.

### **Billing**

*   **GET** `/billing/addresses` - List Billing Addresses
*   **POST** `/billing/addresses` - Create Billing Address
*   **GET** `/billing/addresses/{address_id}` - Get Billing Address
*   **PATCH** `/billing/addresses/{address_id}` - Update Billing Address
*   **DEL** `/billing/addresses/{address_id}` - Delete Billing Address
*   **GET** `/billing/invoices` - List Invoices
*   **GET** `/billing/invoices/{invoice_id}` - Get Invoice
*   **POST** `/billing/invoices/{invoice_id}/credit_card_payment` - Record a Credit Card Payment
*   **PATCH** `/billing/invoices/{invoice_id}/paypal_subscription` - Update a PayPal Subscription
*   **POST** `/billing/invoices/{invoice_id}/paypal_subscription` - Create a PayPal Subscription
*   **GET** `/billing/invoices/{invoice_id}/pdf` - Download Invoice PDF
*   **GET** `/billing/payment_methods` - List Payment Methods
*   **POST** `/billing/payment_methods` - Add Credit Card
*   **GET** `/billing/payment_methods/{method_id}` - Get Payment Method
*   **DEL** `/billing/payment_methods/{method_id}` - Delete Payment Method
*   **PATCH** `/billing/payment_methods/{method_id}` - Update Payment Method
*   **POST** `/billing/payment_methods/credit_card/setup_intent` - Create Credit Card Setup Intent
*   **GET** `/billing/products` - List Available Products

### **Authentication**

*   **POST** `/login` - Authenticate user and generate JWT token

### **Sites**

*   **GET** `/sites` - List sites
*   **POST** `/sites` - Create new site
*   **GET** `/sites/{id}` - Get information about site from system
*   **DEL** `/sites/{id}` - Delete site from system
*   **PATCH** `/sites/{id}` - Update site properties
*   **POST** `/sites/{id}/access_token` - Generate token valid for accessing site operations
*   **GET** `/sites/all/locations` - List Site locations (including restricted)
*   **POST** `/sites/{id}/clone` - Clone a site (via background task)
*   **GET** `/sites/{id}/credentials` - Get password and username for site
*   **GET** `/sites/locations` - List Site locations
*   **POST** `/sites/{id}/lock` - Lock a site so that no modifications can be made
*   **DEL** `/sites/{id}/lock` - Unlock a site so that modifications can be made again
*   **GET** `/sites/{id}/pma_login` - Get SSO link for phpMyAdmin account
*   **GET** `/sites/{id}/settings` - Get site settings
*   **PATCH** `/sites/{id}/settings` - Update site settings
*   **POST** `/sites/{id}/staging` - Create new staging site for given site (via background task)
*   **DEL** `/sites/{id}/staging` - Delete staging site for given site
*   **POST** `/sites/{id}/staging/publish` - Publish staging site as an active site (via background task)
*   **GET** `/sites/{id}/tasks` - List Site Tasks
*   **GET** `/sites/{id}/usage` - Get site usage

### **Site Templates**

*   **POST** `/site-templates/task` - Create new site template
*   **GET** `/sites/templates` - List Site Templates
*   **POST** `/sites/templates` - [Deprecated]: Create new site template
*   **GET** `/sites/templates/{id}` - Get Site Templates
*   **DEL** `/sites/templates/{id}` - Delete Site Templates
*   **POST** `/sites/templates/{id}/sites` - Create new site from a site template

### **Domains**

*   **GET** `/sites/{id}/domains` - List additional domains (aliases) for the site
*   **POST** `/sites/{id}/domains` - Create additional domain
*   **DEL** `/sites/{id}/domains/{domain_id}` - Delete additional domain
*   **GET** `/sites/{id}/maindomain` - Get site main domain info
*   **GET** `/sites/{id}/domains/{domain_id}/edge-settings` - Get additional domain Edge Settings
*   **POST** `/sites/{id}/maindomain` - Set a domain for a Site
*   **PATCH** `/sites/{id}/domains/{domain_id}/edge-settings` - Update additional domain Edge Settings
*   **PATCH** `/sites/{id}/maindomain` - Update maindomain validation method or SSL CA
*   **PUT** `/sites/{id}/maindomain` - Replace current maindomain with different one
*   **PATCH** `/sites/{id}/maindomain/prefix` - Change existing prefix for domain
*   **GET** `/sites/{id}/maindomain/recheck` - Force validation status recheck
*   **GET** `/sites/{id}/maindomain/status` - Checks the status of the maindomain, any alternate maindomains, and additional domains
*   **GET** `/sites/{id}/maindomain/edge-settings` - Get Maindomain Edge Settings
*   **PATCH** `/sites/{id}/maindomain/edge-settings` - Update Maindomain Edge Settings

### **CDN Cache**

*   **POST** `/sites/{id}/cache/purge` - Purge files from cache on cloudflare
*   **POST** `/sites/{id}/cache/purge_everything` - Purge all files from single domain from cache on cloudflare

### **FTP Accounts**

*   **GET** `/sites/{id}/ftp-accounts` - List Ftp Accounts
*   **POST** `/sites/{id}/ftp-accounts` - Create new ftp account
*   **PATCH** `/sites/{id}/ftp-accounts` - Update ftp account
*   **DEL** `/sites/{id}/ftp-accounts` - Delete ftp account

### **Plugins**

*   **GET** `/sites/{id}/featured_plugins` - List available featured plugins
*   **GET** `/sites/{id}/plugins` - List installed WordPress plugins on account
*   **POST** `/sites/{id}/plugins` - Install new WordPress plugins to site
*   **PATCH** `/sites/{id}/plugins` - Activate or deactivate WordPress plugins on given site
*   **PUT** `/sites/{id}/plugins` - Update WordPress plugins on given site
*   **DEL** `/sites/{id}/plugins` - Delete WordPress plugins from given site
*   **GET** `/sites/{id}/plugins/search` - Search for WordPress plugins that can be installed
*   **POST** `/sites/{id}/plugins/rocket_cdn_cache_management` - Install / re-install the Rocket CDN Cache Management plugin

### **Themes**

*   **GET** `/sites/{id}/themes` - List installed Wordpress themes on account
*   **POST** `/sites/{id}/themes` - Install new WordPress themes to site
*   **PATCH** `/sites/{id}/themes` - Activate or deactivate WordPress themes on given site
*   **PUT** `/sites/{id}/themes` - Update WordPress themes on given site
*   **DEL** `/sites/{id}/themes` - Delete WordPress theme from site
*   **GET** `/sites/{id}/themes/search` - Search for WordPress themes that can be installed

### **Reporting**

*   **GET** `/reporting/sites/{id}/cdn/requests` - Retrieve CDN requests report
*   **GET** `/reporting/sites/{id}/cdn/cache-status` - Retrieve CDN cache-status report
*   **GET** `/reporting/sites/{id}/cdn/cache-content` - Retrieve CDN cache-content report
*   **GET** `/reporting/sites/{id}/cdn/cache-top` - [Deprecated] Retrieve cdn cache-top report
*   **GET** `/reporting/sites/{id}/visitors` - Retrieve cdn visitors report
*   **GET** `/reporting/sites/{id}/waf/eventlist` - List WAF Events
*   **GET** `/reporting/sites/{id}/waf/events/source` - Retrieve WAF events source report
*   **GET** `/reporting/sites/{id}/waf/firewall-events` - Retrieve WAF firewall events report
*   **GET** `/reporting/sites/{id}/waf/events/services` - Retrieve WAF events services report
*   **GET** `/reporting/sites/{id}/waf/events/time` - Retrieve WAF events time report
*   **GET** `/reporting/sites/{id}/waf/events` - [Deprecated]: List WAF Events
*   **GET** `/reporting/sites/{id}/bandwidth/top-usage` - Get top usage bandwidth report
*   **GET** `/reporting/sites/{id}/bandwidth/usage` - Get usage bandwidth report
*   **GET** `/sites/{id}/access-logs` - List Access Logs
*   **GET** `/sites/{id}/access_logs` - [Deprecated] List Access Logs
*   **GET** `/sites/{id}/reporting/cdn-request-volume-by-source` - CDN Request Volume by Source
*   **GET** `/sites/{id}/reporting/total-requests` - Total requests from all sources

### **SSH Keys**

*   **GET** `/sites/{id}/ssh-keys` - List SSH keys for given site
*   **POST** `/sites/{id}/ssh-keys` - Import SSH key for given site
*   **DEL** `/sites/{id}/ssh-keys` - Delete SSH key for given site
*   **POST** `/sites/{id}/ssh-keys/authorize` - Activate SSH key for given site
*   **POST** `/sites/{id}/ssh-keys/deauthorize` - Deactivate SSH key for given site
*   **GET** `/sites/{id}/ssh-keys/{name}` - View SSH key info for given site

### **Visitors**

*   **GET** `/account/visitors` - Get unique visitors statistics for user account
*   **GET** `/sites/{id}/visitors` - Get unique visitors statistics for given site

### **Bandwidth**

*   **GET** `/account/bandwidth` - Get bandwidth usage statistics for user account
*   **GET** `/sites/{id}/reporting/bandwidth` - Get bandwidth usage statistics for given site

### **Backups**

*   **POST** `/sites/{id}/backup` - Create a new backup for given site
*   **GET** `/sites/{id}/backup` - Get a list of backups for site
*   **GET** `/sites/{id}/backup/{backup_id}` - Download given backup for site
*   **DEL** `/sites/{id}/backup/{backup_id}` - Delete given backup for site from the system
*   **POST** `/sites/{id}/backup/{backup_id}/restore` - Restore a backup for given site (via background task)
*   **GET** `/sites/{id}/backup/automated` - List automated backups
*   **POST** `/sites/{id}/backup/automated/{restore_id}/restore` - Restore existing automated restore point (via background task)
*   **POST** `/sites/{id}/backup/automated/{restore_id}/restore-database` - Restore existing automated restore point database
*   **POST** `/sites/{id}/backup/automated/{restore_id}/restore-files` - Restore existing automated restore point files
*   **GET** `/sites/{id}/cloud-backups` - List cloud backups
*   **POST** `/sites/{id}/cloud-backups` - Create a new cloud backup
*   **GET** `/sites/{id}/cloud-backups/{backup_id}` - Get a cloud backup
*   **DEL** `/sites/{id}/cloud-backups/{backup_id}` - Delete a cloud backup
*   **GET** `/sites/{id}/cloud-backups/{backup_id}/download` - Get Cloud Backup Download Link
*   **POST** `/sites/{id}/cloud-backups/{backup_id}/restore` - Restore cloud backup / Create new site from backup

### **Files**

*   **GET** `/sites/{id}/file-manager/files` - List Site Files
*   **GET** `/sites/{id}/files` - [Deprecated] List files in a site installation
*   **POST** `/sites/{id}/files` - Upload a file to the site installation
*   **PUT** `/sites/{id}/files` - Save contents of a file to the site installation
*   **DEL** `/sites/{id}/files` - Delete file from a site installation
*   **POST** `/sites/{id}/files/extract` - Extract a file
*   **POST** `/sites/{id}/files/compress` - Compress files or folders
*   **PATCH** `/sites/{id}/files/chmod` - Change file permissions
*   **GET** `/sites/{id}/files/download` - Download contents of a given file
*   **POST** `/sites/{id}/files/folder` - Create folder in a site installation
*   **GET** `/sites/{id}/files/view` - View contents of a given file

### **Account**

*   **POST** `/request_cancel_account` - Request that your Rocket.net account be cancelled
*   **GET** `/hosting_plan` - Get Current Hosting Plan
*   **PUT** `/hosting_plan` - Change Account's Hosting Plan
*   **POST** `/hosting_plan` - Set Hosting Plan
*   **GET** `/account/me` - Get user information
*   **PATCH** `/account/me` - Update user account settings
*   **GET** `/account/usage` - Get unique usage statistics for user account
*   **POST** `/account/billing/sso` - Get a cookie to allow for access to billing data
*   **POST** `/account/password` - Set a new password for your account
*   **GET** `/account/tasks` - Get a list of account level tasks

### **Activity**

*   **POST** `/sites/{id}/activity/disable` - Stops events logging
*   **POST** `/sites/{id}/activity/enable` - Starts events logging
*   **POST** `/sites/{id}/activity/events` - Insert new event into system
*   **GET** `/sites/{id}/activity/events` - List Activity Events
*   **GET** `/sites/{id}/activity/events/{event_id}` - Get event for a site installation with event id
*   **DEL** `/sites/{id}/activity/events/{event_id}` - Delete event from a site installation

### **Site Users**

*   **GET** `/sites/{id}/users` - List all the site users for a Site
*   **POST** `/sites/{id}/users` - Send invite to site user
*   **GET** `/sites/{id}/users/accept` - Accept invite to site
*   **POST** `/sites/{id}/users/accept` - Accept invite to site
*   **DEL** `/sites/{id}/users/{user_id}` - Remove site access for site user
*   **POST** `/sites/{id}/users/{user_id}/reinvite` - Send re-invite to site user
*   **POST** `/sites/users` - Create new site user
*   **GET** `/sites/users` - List all the site for user
*   **POST** `/sites/users/login` - Login as a site user
*   **POST** `/sites/users/reset-password` - Reset password for the site user
*   **PATCH** `/sites/users/{user_id}` - Update site user
*   **POST** `/sites/users/{user_id}/password` - Create or update password for the site user

### **Password Protection**

*   **GET** `/sites/{id}/password-protection` - Get site password protection status
*   **POST** `/sites/{id}/password-protection` - Enable site password protection
*   **DEL** `/sites/{id}/password-protection` - Disable site password protection
*   **GET** `/sites/{id}/password-protection/users` - List site password protection users
*   **POST** `/sites/{id}/password-protection/users` - Add site password protection user
*   **DEL** `/sites/{id}/password-protection/users/{user_id}` - Remove site password protection user

### **Password Strength**

*   **POST** `/password/strength` - Check strength of the given password
*   **POST** `/users/password/strength` - Check strength of the given password

### **Account Users**

*   **POST** `/users` - Create new user who can access your Rocket.net account
*   **GET** `/users` - List all users in your account
*   **DEL** `/users/{user_id}` - Remove a User from your account
*   **GET** `/users/{user_id}` - Get information about a specific user in your account
*   **PATCH** `/users/{user_id}` - Update user
*   **POST** `/users/{user_id}/password` - Create first time password for the Account User
*   **POST** `/users/{user_id}/reinvite` - Re-send invite email to User
*   **GET** `/users/accept` - Accept an invitation to help manage a Rocket.net account

### **ShopShield**

*   **GET** `/sites/{id}/shopshield` - List ShopShield URIs for a site
*   **POST** `/sites/{id}/shopshield` - Enable ShopShield for a URI
*   **DEL** `/sites/{id}/shopshield/{id}` - Disable ShopShield for a URI
*   **GET** `/sites/{id}/shopshield/{id}` - Get ShopShield URI Details

### **WordPress**

*   **POST** `/sites/{id}/cli` - Execute cli command on wp installation ([Deprecated])
*   **GET** `/sites/{id}/wp_login` - Get SSO link for wordpress account
*   **GET** `/sites/{id}/wp/status` - Get Status of WordPress for the site
*   **POST** `/sites/{id}/wpcli` - Execute wp cli command on site
