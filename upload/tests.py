import os
from django.test import TestCase
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User
from .views import weight_data

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
