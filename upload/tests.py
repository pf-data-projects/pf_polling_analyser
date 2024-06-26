"""A test module for the upload app"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Standard library
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from django.test import TestCase
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User

import pandas as pd


class TestWeighting(TestCase):
    """
    A test suite to cover the features of the weighting module.
    """


    def setUp(self):
        """
        Creates test user for test suite
        """
        self.test_user = User.objects.create_user(username='testuser', password="testpassword")
        self.test_user_id = self.test_user.id


    def test_unweighted_results(self):
        """
        This test checks that when you submit data
        to be processed without weighting
        1. the data appears in the cache
        2. the data contains a column 'weighted_respondents'
        with '1' for all values.
        """
        # test login works correctly
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login)

        # test the submission of the weight form and cache key existence.
        file_path = os.path.join(os.path.dirname(__file__), 'data2.xlsx')
        with open(file_path, 'rb') as file:
            xlsx_file = SimpleUploadedFile(
                'data2.xlsx',
                file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        form_data = {
            'results': xlsx_file,
            'apply_weights': False,
            'custom_weights': False,
        }

        response = self.client.post(reverse('weight_data'), form_data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cache.has_key(f"weights_for_user_{self.test_user_id}"))

        # test the weighted file has the correct column
        data = cache.get(f"weights_for_user_{self.test_user_id}")
        df = pd.read_excel(data)
        self.assertTrue('weighted_respondents' in df.columns)
        self.assertTrue((df['weighted_respondents'] == 1).all())


    def test_standard_weights(self):
        """
        This test checks that when you submit data
        to be processed with standard weighting
        1. the data appears in the cache.
        2. the data contains a column 'weighted_respondents'.
        with not '1' for all values.
        """
        # test login works correctly
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login)

        # test the submission of the weight form and cache key existence.
        data_file_path = os.path.join(os.path.dirname(__file__), 'data2.xlsx')
        with open(data_file_path, 'rb') as file:
            xlsx_file = SimpleUploadedFile(
                'data2.xlsx',
                file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        props_file_path = os.path.join(os.path.dirname(__file__), 'Weight_Proportions.xlsx')
        with open(props_file_path, 'rb') as file:
            props_file = SimpleUploadedFile(
                'Weight_Proportions.xlsx',
                file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        form_data = {
            'results': xlsx_file,
            'weights': props_file,
            'apply_weights': True,
            'custom_weights': False,
        }

        response = self.client.post(reverse('weight_data'), form_data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cache.has_key(f"weights_for_user_{self.test_user_id}"))

        # test the weighted file has the correct column
        data = cache.get(f"weights_for_user_{self.test_user_id}")
        df = pd.read_excel(data)
        self.assertTrue('weighted_respondents' in df.columns)
        self.assertTrue((df['weighted_respondents'] != 1).all())


    def test_custom_weights(self):
        """
        A test to check that entering custom weightings
        and running the weight module returns weighted
        data with non-1 values.
        """
        # test login works correctly
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login)

        # test the submission of the weight form and cache key existence.
        data_file_path = os.path.join(os.path.dirname(__file__), 'data.xlsx')
        with open(data_file_path, 'rb') as file:
            xlsx_file = SimpleUploadedFile(
                'data.xlsx',
                file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        props_file_path = os.path.join(
            os.path.dirname(__file__), 'Weight_Proportions_Businesses.xlsx'
        )
        with open(props_file_path, 'rb') as file:
            props_file = SimpleUploadedFile(
                'Weight_Proportions_Businesses.xlsx',
                file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        form_data = {
            'results': xlsx_file,
            'weights': props_file,
            'apply_weights': False,
            'custom_weights': True,
        }

        formset_data = {
            'weights-TOTAL_FORMS': '2',
            'weights-INITIAL_FORMS': '0',
            'weights-MIN_NUM_FORMS': '0',
            'weights-MAX_NUM_FORMS': '1000',

            # First weighting category
            'weights-0-group':'province',
            'weights-0-question':'Province',

            # First weighting category
            'weights-1-group':'size',
            'weights-1-question':'Size'
        }

        data = {**form_data, **formset_data}

        response = self.client.post(reverse('weight_data'), data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cache.has_key(f"weights_for_user_{self.test_user_id}"))

        # test the weighted file has the correct column
        data = cache.get(f"weights_for_user_{self.test_user_id}")
        df = pd.read_excel(data)
        self.assertTrue('weighted_respondents' in df.columns)
        self.assertTrue((df['weighted_respondents'] != 1).all())


class TestCrossbreaks(TestCase):
    """
    A test suite to mock the data processing handled by celery.

    WARNING: make sure you have changed the celery settings in settings.py
    before running this testcase or it will probably do something
    strange and fail.
    """

    def setUp(self):
        """
        Creates test user for test suite
        """
        self.test_user = User.objects.create_user(username='testuser', password="testpassword")


    def test_standard_cb(self):
        """
        Tests a user's submission which only opts for standard
        crossbreaks.
        """
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login)

        data_file_path = os.path.join(os.path.dirname(__file__), 'weighted_data (18).xlsx')
        with open(data_file_path, 'rb') as file:
            xlsx_file = SimpleUploadedFile(
                'weighted_data (18).xlsx',
                file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        form_data = {
            'data_file': xlsx_file,
            'survey_id': 7387003,
            'standard_cb': ['gender', 'age', 'region'],
        }

        formset_data = {
            'crossbreaks-TOTAL_FORMS': '1',
            'crossbreaks-INITIAL_FORMS': '0',
            'crossbreaks-MIN_NUM_FORMS': '0',
            'crossbreaks-MAX_NUM_FORMS': '1000',
        }

        data = {**form_data, **formset_data}

        response = self.client.post(reverse('upload_data'), data, format='multipart', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cache.has_key(f"table_task_id"))
