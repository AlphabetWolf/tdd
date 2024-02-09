"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase
from src.counter import app         # we need to import the unit under test - counter
from src import status              # we need to import the file that contains the status codes


class CounterTest(TestCase):
    def setUp(self):
        """Prepare test case"""
        self.client = app.test_client()

    """Counter tests"""
    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        # Create a counter
        create_result = self.client.post('/counters/foo')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)

        # Check the initial value
        baseline_result = self.client.get('/counters/foo')
        baseline_value = baseline_result.json['foo']

        # Update the counter
        update_result = self.client.put('/counters/foo')
        self.assertEqual(update_result.status_code, status.HTTP_200_OK)

        # Check the updated value
        updated_result = self.client.get('/counters/foo')
        updated_value = updated_result.json['foo']
        self.assertEqual(updated_value, baseline_value + 1)

    def test_read_a_counter(self):
        """It should read a counter"""
        # Create a counter
        self.client.post('/counters/test')

        # Read the counter
        result = self.client.get('/counters/test')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.json['test'], 0)

    def test_delete_a_counter(self):
        """It should delete an existing counter"""
        # First, create a counter to delete
        create_result = self.client.post('/counters/test_counter')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)

        # Now, delete the counter
        delete_result = self.client.delete('/counters/test_counter')
        self.assertEqual(delete_result.status_code, status.HTTP_204_NO_CONTENT)

        # Optionally, verify that the counter no longer exists by making a GET request
        get_result = self.client.get('/counters/test_counter')
        self.assertEqual(get_result.status_code, status.HTTP_404_NOT_FOUND)
