import os
import yaml
import discord


class TestCaseDiscordClient:

    @classmethod
    def setup_class(cls):
        """Setup any test variables."""
        cls.client = discord.Client()
        with open(os.path.abspath('config.yaml'), 'r') as config_file:
            cls.credentials = yaml.safe_load(config_file)

    def test_client_connection(self):
        """
        Checks to see if a valid Discord Client class object exists.
        :return:
        """
        assert self.client

    def test_credentials_read(self):
        """
        Checks to see if credentials have been passed for each API in the credentials file (discord, gspread, etc.)
        :return:
        """
        assert [self.credentials[service] for service in self.credentials.keys()]
