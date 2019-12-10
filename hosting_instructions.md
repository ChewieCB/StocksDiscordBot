# Hosting on Heroku

## Heroku
### 1 - Sign up for a heroku account if you don't already have one
https://signup.heroku.com/
## Local Repo
### 2 - Make sure your config.yaml and google_credentials.json are correctly filled out
### 3 - TEMPORARILY Remove the config.yaml and google_credentials.json from the .gitignore file
We need to have these in the heroku build for the bot to work.
### 4 - Push the config and google credential files to your LOCAL git repo for the bot
Pushing these files to a public Github repo is **strongly advised against** to protect your API keys
## Terminal/Command Line
### 5 - Open the terminal and cd into the project directory (/StocksDiscordBot) if that isn't already the active directory
e.g. 
```
cd PycharmProjects/StocksDiscordBot (or wherever your local repo is saved)
```
### 6 - Make sure the Heroku CLI is installed on your system
https://devcenter.heroku.com/articles/getting-started-with-python#set-up
### 7 - Enter the following commands into the terminal
#### heroku login
then log in to your Heroku account as prompted
#### heroku create *{put a unique dyno name here, e.g. stockbot-123}*
### git push heroku master
then wait for the build to finish
### heroku ps:scale main=1
to check if the bot is running
### heroku logs --tail
this will give you a readout of the dyno, if all is working you will see something along the lines of:
 ```
heroku[main.1]: Starting process with command `python bot.py`
heroku[main.1]: State changed from starting to up
app[main.1]: StockBot#0810 has connected to BotTesting

