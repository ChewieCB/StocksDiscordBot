# StocksDiscordBot

Developed by **Jack McCaffrey** for **Austin Bouley**.

## Setup
### 1 - Create a Discord bot
This is detailed here:
	https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
	
#### Ensure you give the bot the correct permissions to create, read and delete messages, and to assign roles.
  
### 2 - Get a Google Drive and Sheets API Key
This is detailed here:
	https://gspread.readthedocs.io/en/latest/oauth2.html
  
Download your API credentials as a JSON file, name it 'google_credentials.json', and put it in the main folder - this should look like:

&nbsp;&nbsp;&nbsp;&nbsp;*StocksDiscordBot/google_credentials.json*
  
### 3 - Add your Discord bot token, Google API key, and the URL of the spreadsheet you want to fill with emails and usernames into the config.yaml file
A blank *config.yaml* file should be in the root directory of the bot (*StocksDiscordBot/config.yaml*) for you to fill out.

### 4 - Share your spreadsheet with the email listed in the google_credentials.json file
This will be in the form "client-email": "xxxxx@xxxxx-xxxxx.iam.gserviceaccount.com", if you do not share the spreadsheet with your API client then the bot cannot access the spreadsheet.

### 5 - Make sure that the bot is at the top of the role hierarchy
The bot can only change the roles of server members lower than itself in the server hierarchy, for best usage put the bot at the top of the role hierarchy for your server.

## Bot Functions
The bot currently has two main functions:
### !assign example@email.com
- This can be used by anyone in the server. 
- If the user is not a premium member then they are given a premium role and their username and provided email is stored in the google sheet.
- If the user is already a premium member then nothing happens.

### !stocks
- This can only be used by the server admin.
- Calling this function returns the current trends of all stocks stored in the *config.yaml* file.

## Important
If you fork this repo, it is **very highly reccomended** that you **do not store** either of your *config.yaml* or *google_credentials.json* files on git - this prevents unauthorised use of your API keys.
