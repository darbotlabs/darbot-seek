"""Mock ollama module for testing when actual ollama is not available."""

class MockClient:
    def __init__(self, host=None, **kwargs):
        self.host = host or "localhost:11434"
    
    def generate(self, model, prompt, **kwargs):
        return {"response": "Mock response from Ollama"}
    
    def chat(self, model, messages, **kwargs):
        return {"message": {"content": "Mock response from Ollama chat"}}
    
    def list(self):
        return {"models": []}
    
    def show(self, model):
        return {"details": {"format": "gguf"}}

# Create the Client class for import compatibility
Client = MockClient