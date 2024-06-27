"""A test module for the excel app"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Standard library
import os
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from django.test import TestCase
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User


class TestTableMaker(TestCase):
    """
    Test suite that checks the functionality of the
    table-maker module.
    """

    def setUp(self):
        """
        Creates test user for test suite
        """
        self.test_user = User.objects.create_user(
            username='testuser', password="testpassword")
        self.test_user_id = self.test_user.id


    def test_table_maker_form(self):
        """
        This test checks that when you submit data
        to be processed without weighting
        1. the data appears in the cache
        2. the data contains a column 'weighted_respondents'
        with '1' for all values.
        """
        # test login works correctly
        login = self.client.login(
            username='testuser', password='testpassword')
        self.assertTrue(login)

        # test the submission of the weight form and cache key existence.
        file_path = os.path.join(
            os.path.dirname(__file__), 'crossbreaks_data (33).csv')
        with open(file_path, 'rb') as file:
            csv_file = SimpleUploadedFile(
                'crossbreaks_data (33).csv',
                file.read(),
                content_type='text/csv'
            )

        form_data = {
            'data_file': csv_file,
        }

        response = self.client.post(
            reverse('scan_table'), form_data, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            cache.has_key(f"rebase_questions_for_user_{self.test_user_id}"))
        file_path = os.path.join(
            os.path.dirname(__file__), 'table_headers (30).json')
        with open(file_path, 'rb') as file:
            json_file = SimpleUploadedFile(
                'table_headers (30).json',
                file.read(),
                content_type='application/json'
            )
        file_path = os.path.join(
            os.path.dirname(__file__), 'crossbreaks_data (33).csv')
        with open(file_path, 'rb') as file:
            csv_file = SimpleUploadedFile(
                'crossbreaks_data (33).csv',
                file.read(),
                content_type='text/csv'
            )

        form_data = {
            'data_file': csv_file,
            'rebased_header_file': json_file,
            'title': "test",
            "dates": "test",
            "start": 38,
            "end": 356,
            "id_column": True,
        }

        formset_data = {
            "form-TOTAL_FORMS": "104",
            "form-INITIAL_FORMS": "104",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
        }

        data = {**form_data, **formset_data}

        response = self.client.post(
            reverse('table_maker', args=[104]), data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            cache.has_key(f"tables_for_user_{self.test_user_id}"))
