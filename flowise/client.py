import requests
from typing import List, Dict, Optional, Generator

class IFileUpload:
    def __init__(self, data: Optional[str], type: str, name: str, mime: str):
        self.data = data
        self.type = type
        self.name = name
        self.mime = mime


class IMessage:
    def __init__(self, message: str, type: str, role: Optional[str] = None, content: Optional[str] = None):
        self.message = message
        self.type = type
        self.role = role
        self.content = content


class PredictionData:
    def __init__(
        self,
        chatflowId: str,
        question: str,
        overrideConfig: Optional[Dict] = None,
        chatId: Optional[str] = None,
        streaming: Optional[bool] = False,
        history: Optional[List[IMessage]] = None,
        uploads: Optional[List[IFileUpload]] = None
    ):
        self.chatflowId = chatflowId
        self.question = question
        self.overrideConfig = overrideConfig
        self.chatId = chatId
        self.streaming = streaming
        self.history = history
        self.uploads = uploads


class Flowise:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or 'http://localhost:3000'
        self.api_key = api_key or ''

    def _get_headers(self) -> Dict[str, str]:
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def create_prediction(self, data: PredictionData) -> Generator[str, None, None]:
        # Step 1: Check if chatflow is available for streaming
        chatflow_stream_url = f'{self.base_url}/api/v1/chatflows-streaming/{data.chatflowId}'
        response = requests.get(chatflow_stream_url)
        response.raise_for_status()
        
        chatflow_stream_data = response.json()
        is_streaming_available = chatflow_stream_data.get("isStreaming", False)

        prediction_url = f'{self.base_url}/api/v1/prediction/{data.chatflowId}'

        # Step 2: Handle streaming prediction
        if is_streaming_available and data.streaming:
            prediction_payload = {
                'chatflowId': data.chatflowId,
                'question': data.question,
                'overrideConfig': data.overrideConfig,
                'chatId': data.chatId,
                'streaming': data.streaming,
                'history': [msg.__dict__ for msg in (data.history or [])],
                'uploads': [upload.__dict__ for upload in (data.uploads or [])]
            }

            with requests.post(prediction_url, json=prediction_payload, stream=True, headers=self._get_headers()) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data:'):
                            event = line_str.replace('data:', '').strip()
                            yield event

        # Step 3: Handle non-streaming prediction
        else:
            prediction_payload = {
                'chatflowId': data.chatflowId,
                'question': data.question,
                'overrideConfig': data.overrideConfig,
                'chatId': data.chatId,
                'history': [msg.__dict__ for msg in (data.history or [])],
                'uploads': [upload.__dict__ for upload in (data.uploads or [])]
            }

            response = requests.post(prediction_url, json=prediction_payload, headers=self._get_headers())
            response.raise_for_status()
            yield response.json()
