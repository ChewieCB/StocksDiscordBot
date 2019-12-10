import yaml
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Authorise gspread with Google Drive and Google Sheets API credentials
# see link for more information -------> https://gspread.readthedocs.io/en/latest/oauth2.html
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name('google_credentials.json', scope)
gc = gspread.authorize(credentials)

# NOTE - you must share the spreadsheet you want to write to with the CLIENT_EMAIL specified in the
# google_credentials.json file, otherwise the API doesn't have access


def write_to_sheet(sheet, email: str, username: str):
    """

    :param sheet: A gspread worksheet object.
    :param email: A valid email string.
    :param username: A valid username string.
    :return: A string for the bot to display on either success or failure.
    """
    # Open the first sheet of the specified google spreadsheet
    sheet = sheet.sheet1
    # Get the existing emails and usernames to check for the next empty row
    existing_emails = sheet.col_values(1)
    existing_usernames = sheet.col_values(2)
    # Check if email or username already exists in list
    if email in existing_emails or username in existing_usernames:
        return "Email and/or username already registered!"
    else:
        # Get the next empty row from the last index of the existing rows
        next_empty_row = len(existing_emails) + 1
        # Add the new email and username to the next empty row (arg order is row number, col number, value)
        sheet.update_cell(next_empty_row, 1, email)
        sheet.update_cell(next_empty_row, 2, username)
        return "Email and username registered"
