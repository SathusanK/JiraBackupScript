from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from glob import glob
from datetime import datetime
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os
import subprocess
import smtplib


def erroremailer():

    mail_from = 'Jira Backup Script <donotreply@email.com>'
    mail_to = 'Some Guy <some.guy@email.com>'

    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = 'Backup Failed'
    mail_body = """
    Hello,

    A failure in the Jira backup script has been detected.
    Please look at Heroku logs for more details.

    """
    msg.attach(MIMEText(mail_body))

    try:
        server = smtplib.SMTP_SSL('smtp.sendgrid.net', 465)
        server.ehlo()
        server.login('apikey', 'SENDGRID API KEY HERE')
        server.sendmail(mail_from, mail_to, msg.as_string())
        server.close()
        print("Mail sent.")
    except:
        print("issue")

    return


def successemailer():

    mail_from = 'Jira Backup Script <donotreply@email.com>'
    mail_to = 'Some Guy <some.guy@email.com>'

    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = 'Backup Successful'
    mail_body = """
    Hello,

    Backup was Successful.
    Always check the drive folder to be sure.

    """
    msg.attach(MIMEText(mail_body))

    try:
        server = smtplib.SMTP_SSL('smtp.sendgrid.net', 465)
        server.ehlo()
        server.login('apikey', 'SENDGRID API KEY HERE')
        server.sendmail(mail_from, mail_to, msg.as_string())
        server.close()
        print("Mail sent.")
    except:
        print("issue")

    return


def backup():
    # Run the backup script
    print("Running the bash backup script...")
    subprocess.call("./JiraBackupScript.txt", shell=True)

    # Initialize all config variables for drive
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh Google auth tokens if expired
        gauth.Refresh()
    else:
        # Initialize the saved credentials
        gauth.Authorize()

    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    currentDir = os.getcwd()  # Saves the default directory in case you need to go back

    os.chdir(currentDir)  # cd's to current directory

    # Get a list of folders in the user's google drive
    driveFileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    backupFolderExists = False
    parentFolderId = ""

    # Create a backup folder in drive if it doesn't already exist & get its parent ID
    for folder in driveFileList:
        if folder['title'] == "Jira Backups":
            print("Backups folder exists in drive")
            parentFolderId = folder['id']
            backupFolderExists = True
            break

    # If the folder does not exist, make one & upload it
    if not backupFolderExists:
        print("Backups folder does not exist in drive.")
        folder1 = drive.CreateFile({'title': 'Jira Backups', "mimeType": "application/vnd.google-apps.folder"})
        folder1.Upload()
        parentFolderId = folder1['id']

    # Upload the Jira backup zip file.yaml to the Drive
    fileToUpload = glob("JIRA-backup*.zip")

    # Attempt to upload the backup file. If it doesn't exist, email the admin and exit.
    try:
        file1 = drive.CreateFile({'title': fileToUpload[0], "parents": [{"kind": "drive#fileLink", "id": parentFolderId}]})
    except:
        print("Failure detected. Notifying administrator.")
        erroremailer()
        return

    file1.SetContentFile(os.getcwd() + "/" + fileToUpload[0])

    file1.Upload()

    # Delete the backup zip file.yaml from the desktop
    print("Running the bash deletion script...")
    sleep(1)
    os.popen('rm `ls | grep JIRA-backup-`')  # Shout out to Hugh
    successemailer()  # this is for testing. Won't be in the final script.
    print("Done!")

    return


# Run the script every day between 11:59:00pm and 11:59:30pm
while True:

    now = datetime.today().now()
    backupTime0 = now.replace(hour=23, minute=59, second=0, microsecond=0)
    backupTime1 = now.replace(hour=23, minute=59, second=5, microsecond=0)

    sleep(1)
    if backupTime0 < now < backupTime1:
        backup()
