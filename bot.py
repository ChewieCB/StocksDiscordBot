#!/usr/bin/env python
import re
import yaml
import discord

from sheet import write_to_sheet
from stocks import check_stocks

# Initialise the discord client
client = discord.Client()
# Read the API keys from the config file
with open('config.yaml', 'r') as config_file:
    credentials = yaml.safe_load(config_file)

# Get list of stocks
stocks_list = [stock.upper() for stock in credentials['STOCKS']]


@client.event
async def on_message(message):
    """
    Wait for a user to post a message, check for the key word "!assign" and an email address, update
    :param message: A message posted in a discord server that the bot is part of.
    :return:
    """
    # Check the message has been sent by a user, to stop the bot replying to itself
    if message.author == client.user:
        return
    if message.content.startswith('!assign'):
        # Use a regex function to search for an email address in the message
        try:
            email_address = re.search(r'[\w\.-]+@[\w\.-]+', message.content).group()
        except AttributeError:
            email_address = None

        if email_address:
            # Find the premium role
            premium_role = [role for role in client.guilds[0].roles if role.name.lower() == 'premium'][0]
            user_roles = message.author.roles
            # Check whether or not the user has the premium role
            if premium_role in user_roles:
                # Alert the user that they are already premium
                await message.channel.send(f"{message.author.mention} You are already a premium member!")
            else:
                # Add the email and username to the spreadsheet
                sheet_response = write_to_sheet(email_address, message.author._user.name)
                if sheet_response == "Email and/or username already registered!":
                    await message.channel.send(f"{message.author.mention} {sheet_response}")
                else:
                    # Upgrade the user role to premium
                    await message.author.add_roles(premium_role)
                    await message.channel.send(f"{message.author.mention} {sheet_response}Welcome to premium!")
        else:
            # Mention the user and prompt them to try again with a valid email
            no_email_msg = "No email found! Please try again with a valid email."
            await message.channel.send(
                f"{message.author.mention} {no_email_msg}"
            )
        # Delete the user's initial message
        await message.delete()
    elif message.content.startswith('!stocks'):
        if message.author.guild_permissions.administrator is True:
            # Retrieve the current stocks
            trending = check_stocks(stocks_list)
            stocks_response = ''.join([
                f"__**{key}**__:\n{', '.join(item)}\n\n" if item else f"__**{key}**__:\n{None}\n\n" for key, item in trending.items()
            ])
            await message.channel.send(stocks_response)
        else:
            await message.channel.send(f'Sorry {message.author.mention}, only the server admin can call that function!')
        # Delete the user's initial message
        await message.delete()


@client.event
async def on_ready():
    print(f'{client.user} has connected to {client.guilds[0].name}')


client.run(credentials['DISCORD']['TOKEN'])
