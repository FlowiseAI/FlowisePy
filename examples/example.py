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

def example_with_history_and_uploads():
    # Initialize Flowise client
    client = Flowise()

    # Example message history
    history = [
        IMessage(content="What is the weather?", role="userMessage"),
        IMessage(content="It is sunny today.", role="apiMessage")
    ]

    # Example file upload
    uploads = [
        IFileUpload(data="base64EncodedData", type="file", name="example.txt", mime="text/plain")
    ]

    # Create a prediction with history and uploads
    completion = client.create_prediction(
        PredictionData(
            chatflowId="abc",
            question="Analyze the attached file.",
            streaming=True,
            history=history,  # Pass message history
            uploads=uploads   # Pass file uploads
        )
    )

    # Process and print each streamed chunk
    print("Streaming response with history and uploads:")
    for chunk in completion:
        print(chunk)


if __name__ == "__main__":
    # Run the non-streaming example
    example_non_streaming()

    # Run the streaming example
    example_streaming()

    # Run the example with history and file uploads
    example_with_history_and_uploads()
