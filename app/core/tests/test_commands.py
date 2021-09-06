from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):

    def test_should_wait_for_db_ready(self):
        # Given
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # When
            gi.return_value = True
            call_command('wait_for_db')

            # Then
            self.assertEqual(gi.call_count, 1)

    """@patch allows for mocking of core python functions"""
    @patch('time.sleep', return_value=True)
    def test_should_wait_for_db(self, timesleep):
        # Given
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # When
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')

            # Then
            self.assertEqual(gi.call_count, 6)
