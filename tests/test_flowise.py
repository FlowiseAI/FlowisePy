import unittest
from unittest.mock import patch, MagicMock
from flowise import Flowise, PredictionData, IMessage, IFileUpload

class TestFlowiseClient(unittest.TestCase):

    @patch('flowise.client.requests.post')
    @patch('flowise.client.requests.get')
    def test_create_prediction_non_streaming(self, mock_get, mock_post):
        # Mock the response for the streaming check (non-streaming scenario)
        mock_get.return_value.json.return_value = {"isStreaming": False}

        # Mock the non-streaming POST response
        mock_post.return_value.json.return_value = {"answer": "The capital of France is Paris."}

        # Create a client instance
        client = Flowise()

        # Make a non-streaming request
        completion = client.create_prediction(
            PredictionData(
                chatflowId="abc",
                question="What is the capital of France?",
                streaming=False
            )
        )

        # Verify the full JSON response
        response = list(completion)
        self.assertEqual(response[0], {"answer": "The capital of France is Paris."})

    @patch('flowise.client.requests.post')
    @patch('flowise.client.requests.get')
    def test_create_prediction_streaming(self, mock_get, mock_post):
        # Mock the response for the streaming check (streaming is available)
        mock_get.return_value.json.return_value = {"isStreaming": True}

        # Mock the streaming POST response
        mock_post.return_value.iter_lines.return_value = [
            b'data: {"event": "token", "data": "Why don\'t scientists trust atoms?"}',
            b'data: {"event": "token", "data": "Because they make up everything!"}'
        ]

        # Create a client instance
        client = Flowise()

        # Make a streaming request
        completion = client.create_prediction(
            PredictionData(
                chatflowId="abc",
                question="Tell me a joke!",
                streaming=True
            )
        )

        # Collect and verify the streamed chunks
        response = list(completion)
        self.assertEqual(response, [
            '{"event": "token", "data": "Why don\'t scientists trust atoms?"}',
            '{"event": "token", "data": "Because they make up everything!"}'
        ])

if __name__ == '__main__':
    unittest.main()
