# Stats Project: Correlation Between Music Listening and Study Habits

### Warning:
The data for the Pandas DataFrame used through the jupyter notebook is obtained using a google service account. The data frame won't be assigned and an error will occur if the JSON file for the google service account is not included in a folder named 'config'.

For Caleb: 

Go to the google cloud website: https://console.cloud.google.com/welcome

Log in with the email that you used to create the Stats form and google sheet.

Open the navigation menu in the top-left (Three Horizontal Lines)

Look for "IAM & Admin" category

Within that category go to "Service Accounts" category

A service account with the name of "sheets-reader-sa" should be shared with you

Open it and go to the "Keys" tab

Select "add key" -> select "Create new key" -> select "JSON" -> select "Create"

add the downloaded JSON key into a folder named "config" and make sure to add the folder to .gitignore