import os
import json
import yaml
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from sheet import write_to_sheet

with open('config.yaml', 'r') as config_file:
    credentials = yaml.safe_load(config_file)

SHEET_URL = credentials['GSPREAD']['SHEET_URL']

# Authorise gspread with Google Drive and Google Sheets API credentials
# see link for more information -------> https://gspread.readthedocs.io/en/latest/oauth2.html
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.abspath('google_credentials.json'), scope)
gc = gspread.authorize(credentials)


class TestCaseSheet:

    @classmethod
    def setup_class(cls):
        """
        Read the test data and create a worksheet for testing use in the spreadsheet.
        :return:
        """
        # Get credentials from config gile
        with open(os.path.abspath('config.yaml'), 'r') as config_file:
            cls.credentials = yaml.safe_load(config_file)
        # Get test data
        with open(os.path.abspath('tests/test_user_data.json'), 'r+') as read_file:
            cls.test_data = json.load(read_file)
        # create a new worksheet and populate it for testing
        cls.sheet = gc.open_by_url(SHEET_URL)
        # If a testing sheet doesn't already exist, create one
        cls.test_worksheet = cls.sheet.add_worksheet(title="Test Sheet", rows="100", cols="20")
        # Add test sheet header columns
        cls.test_worksheet.update_cell(1, 1, 'Email')
        cls.test_worksheet.update_cell(1, 2, 'Username')

    @classmethod
    def teardown_class(cls):
        """
        Delete the test worksheet once the tests have been run.
        :return:
        """
        cls.sheet = gc.open_by_url(SHEET_URL)
        cls.sheet.del_worksheet(cls.sheet.worksheet('Test Sheet'))

    def test_sheet_credentials(self):
        """Check that the Google API credentials are valid and that the sheet can be opened."""
        assert self.sheet
        assert self.test_worksheet

    def test_write_to_sheet(self):
        """
        Check that each test email and test username is written to the sheet successfully.
        :return:
        """
        assert [write_to_sheet(user['email'], user['username']) for user in self.test_data]

    def test_existing_user(self):
        """
        Check that the function recognises pre-existing emails and usernames.
        :return:
        """
        for user in self.test_data:
            assert write_to_sheet(user['email'], user['username']) \
                   == "Email and/or username already registered!"
