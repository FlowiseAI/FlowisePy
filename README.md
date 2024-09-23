# Flowise SDK - Python

The **Flowise SDK** for Python provides an easy way to interact with the Flowise API for creating predictions, supporting both streaming and non-streaming responses. This SDK allows users to create predictions with customizable options, including history, file uploads, and more.

## Features

- Support for streaming and non-streaming API responses
- Ability to include message history and file uploads

## Installation

You can install the SDK via pip:

```bash
pip install flowise
```

Upgrade version:

```bash
pip install --upgrade flowise
```

## Example

```py
from flowise import Flowise, PredictionData, IMessage, IFileUpload

def example_non_streaming():
    # Initialize Flowise client
    client = Flowise()

    # Create a prediction without streaming
    completion = client.create_prediction(
        PredictionData(
            chatflowId="abc",
            question="What is the capital of France?",
            streaming=False  # Non-streaming mode
        )
    )

    # Process and print the full response
    for response in completion:
        print("Non-streaming response:", response)

def example_streaming():
    # Initialize Flowise client
    client = Flowise()

    # Create a prediction with streaming enabled
    completion = client.create_prediction(
        PredictionData(
            chatflowId="abc",
            question="Tell me a joke!",
            streaming=True  # Enable streaming
        )
    )

    # Process and print each streamed chunk
    print("Streaming response:")
    for chunk in completion:
        print(chunk)


if __name__ == "__main__":
    # Run the non-streaming example
    example_non_streaming()

    # Run the streaming example
    example_streaming()
```

## Build & Publish

1. Increment version on `setup.py`
1. `pip install wheel`
2. `python setup.py sdist bdist_wheel`
3. `twine upload --skip-existing dist/*`
