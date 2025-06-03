"""Mock openai module for testing when actual openai is not available."""

class MockChoice:
    def __init__(self):
        self.message = MockMessage()

class MockMessage:
    def __init__(self):
        self.content = "Mock response from OpenAI"

class MockResponse:
    def __init__(self):
        self.choices = [MockChoice()]

class MockCompletions:
    def create(self, **kwargs):
        return MockResponse()

class MockChat:
    def __init__(self):
        self.completions = MockCompletions()

class MockClient:
    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key
        self.chat = MockChat()

# Create the OpenAI class for import compatibility
OpenAI = MockClient