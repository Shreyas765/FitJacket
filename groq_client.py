import os
from groq import Groq
from threading import Lock

class GroqClientSingleton:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GroqClientSingleton, cls).__new__(cls)
                    cls._instance._client = Groq(
                        api_key="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"
                    )
        return cls._instance
    
    @property
    def client(self):
        return self._client
    
    def get_chat_completion(self, messages, model="llama-3.3-70b-versatile"):
        return self._client.chat.completions.create(
            messages=messages,
            model=model
        ) 