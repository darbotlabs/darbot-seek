"""Mock httpx module for testing when actual httpx is not available."""

class MockResponse:
    def __init__(self, status_code=200, text="", json_data=None):
        self.status_code = status_code
        self.text = text
        self._json_data = json_data or {}
    
    def json(self):
        return self._json_data

class MockClient:
    def __init__(self, **kwargs):
        pass
    
    def post(self, url, **kwargs):
        return MockResponse(200, "Mock response")
    
    def get(self, url, **kwargs):
        return MockResponse(200, "Mock response")
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

# Mock the main httpx functions
def post(url, **kwargs):
    return MockResponse(200, "Mock response")

def get(url, **kwargs):
    return MockResponse(200, "Mock response")

Client = MockClient