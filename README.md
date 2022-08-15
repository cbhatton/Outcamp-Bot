# Outcamp Bot

to set up outcampbot you will have to create a google cloud project and corisponding credentials:

## Creating Cloud Project
1. go to Google Cloud [console](https://console.cloud.google.com/welcome) and create a new project making sure to add the orginization you with to use
2. Select the project then navigate to APIs and Services > OAuth Consent Screen
3. Frm here select **internal** and fill out the following forms
4. Next go APIs and **Services > Credentials** and click **Create New Credentials > OAuth Client ID** 
5. Download that json file, you'll need it in a second
### Setting up the project
7. Clone or download the project from github]
8. Find the folder **dist/auth/** where you will add two new files
	- settings.json with the format `{"sheet_id": <sheet_id>}` (find the sheet id in the url of the spreadsheet you would like to use then paste it here)
	- credentials.json (use the json file you grabed in step 5)
9. If you run the **main.exe** file in **dist** folder you the program should run and start scanning
