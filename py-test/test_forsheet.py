"""
Test suite for the forsheet module, covering the generate and lecture functions.

This test file employs the unittest module to conduct unit tests for the forsheet functions.
It utilizes the unittest.mock.patch decorator to isolate external dependencies and simulate
responses from OpenAI, allowing controlled testing of the generate and lecture functions.

Test Functions:
- `test_generate`: Verifies the correctness of the generate function by mocking OpenAI's response
                  and asserting that the generated formula matches the expected result.

- `test_lecture`: Verifies the correctness of the lecture function by mocking OpenAI's response
                  and asserting that the generated explanation is not empty.

Note: For each test, the responses from OpenAI are simulated using the unittest.mock.patch decorator.
The test functions use specific test inputs to ensure the functions produce the expected results.

To Run Tests:
- Execute the script directly to run all the tests within this file.

Usage:
    $ python test_forsheet.py

"""

import unittest
from unittest.mock import patch
from forsheets import generate, lecture


class TestForsheetFunctions(unittest.TestCase):

    @patch('openai.OpenAI')
    def test_generate(self, mock_openai):
        """Test the generate function."""
        # Mock the response from OpenAI
        mock_response = mock_openai.return_value.chat.completions.create.return_value
        mock_response.choices = [{"message": {"content": "=SUM(A1:A10)"}}]

        # Call the generate function with a test input
        user_input = "Add the values in cells A1 to A10"
        formula = generate(user_input)

        # Assert that the generated formula is correct
        self.assertEqual(formula, '"=SUM(A1:A10)"')

    @patch('openai.OpenAI')
    def test_lecture(self, mock_openai):
        """Test the lecture function."""
        # Mock the response from OpenAI
        mock_response = mock_openai.return_value.chat.completions.create.return_value
        mock_response.choices = [
            {"message": {"content": "This formula calculates the average of the values in cells B2:B10"}}]

        # Call the lecture function with a test input
        user_input = "=AVERAGE(B2:B10)"
        explanation = lecture(user_input)

        # Assert that the explanation is not empty
        self.assertNotEqual(explanation, '""')


if __name__ == '__main__':
    unittest.main()
