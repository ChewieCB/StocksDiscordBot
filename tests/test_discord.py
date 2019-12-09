import yaml
import pytest
import discord

from bot import on_message


class TestCaseDiscordClient:

    @classmethod
    def setup_class(cls):
        """Setup any test variables."""
        cls.client = discord.Client()
        with open('config.yaml', 'r') as config_file:
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

    def test_no_self_reply(self):
        """"""
        # TODO
        pass
        # we don't want the bot replying to itself
        # assert not on_message()

    def test_message_detection(self):
        """"""
        # TODO
        pass

    def test_detect_assign_command(self):
        """"""
        # TODO
        pass

    def test_get_user_data(self):
        """"""
        # TODO
        pass

    def test_assign_role(self):
        """"""
        # TODO
        pass

    def test_delete_original_message(self):
        """"""
        # TODO
        pass
