README
------
[Feedback is appreciated]

Script 0: Main.py

Description: Core function is to authenticate Google credentials with Drive API and run Bash backup script.
             Can also:
                        - Check for an existing backup container folder and creates one if it does not exist
                        Remove local copy of backup files after upload to cloud.

                        - Send emails using Sendgrid in the event of a failure or when backup finishes successfully.

USAGE: run Main.py
ex. in command line -> "python Main.py" or "python3 Main.py"


Google Auth Requirements listed in the doc below:
(Will be listed at a later date due to an NDA)


File System Requirements
--------------------------
Files to include in same folder:

"Main.py"
"Procfile"
"client_secrets.json"
"credentials.json"
"JiraBackupScript.txt"
"mycreds.txt"
"requirements.txt"
"settings.yaml"
"readme.txt"


client_secrets.json Requirements
----------------------------------
This entire file can be downloaded via your Google API dashboard once you've set up API access.

client_id: Client ID number provided by Google
project_id: Project ID number provided by Google
auth_uri: Authorization URI provided by Google
token_uri: Token URI provided by Google
auth_provider_x509_cert_url: Authorization Provider URL provided by Google
client_secret: Client secret provided by Google
redirect_uris: Redirect URI's provided by Google.

example:
{
  "installed": {
    "client_id": "egfberwjkgbrewkgbqekbwghkeqgheqgk.apps.googleusercontent.com",
    "project_id": "jira-backup-script",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "ffrerehqjgbekqqhq",
    "redirect_uris": [
      "urn:ietf:wg:oauth:2.0:oob",
      "http://localhost"
    ]
  }
}


mycreds.txt Requirements
--------------------------
This file is to be left empty until first (and only) Google authorization.


Procfile Requirements
-----------------------
<process type>: <command>
process type: name for your command such as web, worker, urgentworker, clock, etc.
command: Indicate the command that the Heroku Dyno should execute on startup.

example:
worker: python Main.py


requirements.txt Requirements
-------------------------------
Specify any 3rd party Python modules that must be installed, followed by the version number you would like installed.
One module name, version per line.

example:
pydrive==1.2.1
oauth2client==3.0.0

settings.yaml Requirements
----------------------------
client_config_file: Path to the file containing client configuration. By default should be 'client_secrets.json'.
save_credentials: True if credentials need to be saved for future use.
save_credentials_backend: Backend to save credentials to. By default should be 'file'.
save_credentials_backend: Destination of credentials file.
oauth_scope: OAuth scope to authenticate. By default is 'https://www.googleapis.com/auth/drive'.

example:
client_config_file: client_secrets.json

save_credentials: True
save_credentials_backend: file
save_credentials_file: credentials.json

oauth_scope:
  - https://www.googleapis.com/auth/drive


Script 1: JiraBackupScript.txt

Description: Core function is to create a backup of Jira data off of Atlassian servers.
             Can also:
                        Do full backups every Tuesday and Friday
                        Do small backups every day in between
                        Download backups to a hardcoded directory

USAGE: can run bash script using conventional methods.
ex. in terminal ->"./JiraBackupScript.txt"


File System Requirements
--------------------------
Files to include in same folder:
"Main.py"
"Procfile"
"client_secrets.json"
"credentials.json"
"JiraBackupScript.txt" (This file)
"mycreds.txt"
"requirements.txt"
"settings.yaml"
"readme.txt"

Configuration requirements
Under Configuration Section
-----------------------------
- Specify EMAIL (your Atlassian email address)
- Specify HOSTNAME (ex. whatever.atlassian.net)
- Specify API_TOKEN from Atlassian
- Specify DOWNLOAD_FOLDER based on whether or not it is being tested or run in Heroku
    ex. $(pwd) for testing; /app for Heroku
- Specify your Atlassian instance's timezone. Currently set to Canada/Central
