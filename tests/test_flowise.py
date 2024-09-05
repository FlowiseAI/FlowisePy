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
            b'data: {"event": "data", "content": "Why don\'t scientists trust atoms?"}',
            b'data: {"event": "data", "content": "Because they make up everything!"}'
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
            '{"event": "data", "content": "Why don\'t scientists trust atoms?"}',
            '{"event": "data", "content": "Because they make up everything!"}'
        ])

    @patch('flowise.client.requests.post')
    @patch('flowise.client.requests.get')
    def test_create_prediction_with_history_and_uploads(self, mock_get, mock_post):
        # Mock the response for the streaming check (streaming is available)
        mock_get.return_value.json.return_value = {"isStreaming": True}

        # Mock the streaming POST response
        mock_post.return_value.iter_lines.return_value = [
            b'data: {"event": "data", "content": "Processing the uploaded file..."}',
            b'data: {"event": "data", "content": "File analysis complete."}'
        ]

        # Create a client instance
        client = Flowise()

        # Example message history and file uploads
        history = [
            IMessage(message="What is the weather?", type="userMessage"),
            IMessage(message="It is sunny today.", type="apiMessage")
        ]
        uploads = [
            IFileUpload(data="base64EncodedData", type="file", name="example.txt", mime="text/plain")
        ]

        # Make a streaming request with history and uploads
        completion = client.create_prediction(
            PredictionData(
                chatflowId="abc",
                question="Analyze the attached file.",
                streaming=True,
                history=history,
                uploads=uploads
            )
        )

        # Collect and verify the streamed chunks
        response = list(completion)
        self.assertEqual(response, [
            '{"event": "data", "content": "Processing the uploaded file..."}',
            '{"event": "data", "content": "File analysis complete."}'
        ])

        # Verify that the history and uploads were included in the POST request
        expected_payload = {
            'chatflowId': 'abc',
            'question': 'Analyze the attached file.',
            'overrideConfig': None,
            'chatId': None,
            'streaming': True,
            'history': [
                {'message': 'What is the weather?', 'type': 'userMessage', 'role': None, 'content': None},
                {'message': 'It is sunny today.', 'type': 'apiMessage', 'role': None, 'content': None}
            ],
            'uploads': [
                {'data': 'base64EncodedData', 'type': 'file', 'name': 'example.txt', 'mime': 'text/plain'}
            ]
        }

        mock_post.assert_called_once_with(
            'http://localhost:3000/api/v1/prediction/abc',
            json=expected_payload,
            stream=True
        )


if __name__ == '__main__':
    unittest.main()
