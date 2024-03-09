"""
Test suite for the Flask application's routes and functionality.

This file utilizes the unittest framework to conduct unit tests for various components
of the Flask application. The tests cover route functionality, template rendering,
user authentication, formula generation, explanation routes, and the daily limit reset job.

Tested Components:
1. Home route redirects appropriately.
2. Home template contains the expected content.
3. Dashboard route behaves correctly for both authenticated and unauthenticated users.
4. Formula route generates the correct formula based on user input.
5. Explain route provides explanations for formulas based on user input.
6. Reset daily limits job resets user counters as expected.

To run the tests, execute this file. The MongoDB database used for testing is configured
to run locally.

Test Class:
- `TestApplication`: Class containing individual test methods for different components
                    of the Flask application.

Test Methods:
- `setUp`: Method to set up the Flask application for testing by configuring the application,
            setting up a test client, and starting the test database.

- `tearDown`: Method to tear down the Flask application after testing by removing the test user
            from the database and killing the test database.

- `create_test_user`: Helper method to create a test user with an optional email.

- `test_home_route`: Verifies the behavior of the home route, expecting a redirect status code.

- `test_home_template`: Verifies the content of the home template, expecting a redirect message.

- `test_dashboard_route_unauthenticated`: Verifies the behavior of the dashboard route for an
                                          unauthenticated user.

- `test_dashboard_route_authenticated`: Verifies the behavior of the dashboard route for an
                                        authenticated user.

- `test_formula_route`: Verifies the behavior of the formula route, checking if the generated
                       formula matches the expected result.

- `test_explain_route`: Verifies the behavior of the explain route, checking if the generated
                       explanation is not empty.

- `test_reset_daily_limits_job`: Verifies the behavior of the reset_daily_limits job, checking
                                 if user counters are reset as expected.

Note: For each test, specific test inputs and assertions are used to ensure the proper functioning
of different components of the Flask application.

Usage:
    $ python test_app.py

"""

import unittest
from faker import Faker
from flask import Flask
from app import app, db, reset_daily_limits
from user.models import User

fake = Faker()


class TestApplication(unittest.TestCase):

    def setUp(self):
        """
                Set up the Flask application for testing.

                - Configures the application for testing.
                - Sets up a test client for making requests.
                - Starts the test database.

        """

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        app.config['MONGODB_SETTINGS'] = {
            'db': 'forsheets',
            'host': 'localhost',
            'port': 27017
        }
        self.app = app.test_client()
        db.start_db()

    def tearDown(self):
        """
                Tear down the Flask application after testing.

                - Removes the test user from the database.
                - Kills the test database.

        """

        User.objects(name='Test User').delete()
        db.kill_db()

    def create_test_user(self, email=None):
        """
                Helper method to create a test user with optional email.

                Args:
                    email (str): Optional email address for the test user.

                Returns:
                    User: Created test user object.

        """

        return User(name='Test User', email=email or fake.email(), password='testpassword')

    def test_home_route(self):
        """Test the behavior of the home route."""

        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Expecting a redirect status code

    def test_home_template(self):
        """Test the content of the home template."""

        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Redirecting', response.data)

    def test_dashboard_route_unauthenticated(self):
        response = self.app.get('/dashboard/', follow_redirects=True)

        # Check if the redirected URL is the expected home.html
        self.assertEqual(response.request.path, '/home')

    def test_dashboard_route_authenticated(self):
        """Test the behavior of the dashboard route for an authenticated user."""

        # Create a user in the test database
        user = self.create_test_user()
        user.save()

        # Login the user
        with self.app.session_transaction() as sess:
            sess['logged_in'] = True
            sess['user'] = {'email': user.email}

        response = self.app.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_formula_route(self):
        """Test the behavior of the formula route."""

        # Create a user in the test database
        user = self.create_test_user(email='test@example.com')
        user.formula_counter = 1
        user.save()

        # Login the user
        with self.app.session_transaction() as sess:
            sess['logged_in'] = True
            sess['user'] = {'email': user.email}

        response = self.app.get('/formula?user_input=Add the values in cells A1 to A10')
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"=SUM(A1:A10)"', response.data)

    def test_explain_route(self):
        """Test the behavior of the explain route."""

        # Create a user in the test database
        user = self.create_test_user(email='test@example.com')
        user.explanation_counter = 1
        user.save()

        # Login the user
        with self.app.session_transaction() as sess:
            sess['logged_in'] = True
            sess['user'] = {'email': user.email}

        response = self.app.get('/explain?user_input==AVERAGE(B2:B10)')
        # print(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, '""')

    def test_reset_daily_limits_job(self):
        """Test the reset_daily_limits job."""

        # Create a user in the test database
        user = self.create_test_user(email='test@example.com')
        user.formula_counter = 2
        user.explanation_counter = 2
        user.save()

        # Run the reset_daily_limits job
        reset_daily_limits()

        # Check if counters are reset
        updated_user = User.objects(email=user.email).first()
        self.assertEqual(updated_user.formula_counter, 5)  # Replace with the expected value
        self.assertEqual(updated_user.explanation_counter, 5)  # Replace with the expected value


if __name__ == '__main__':
    unittest.main()
