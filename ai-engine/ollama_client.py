"""
Ollama client for Guardian AI engine.
Communicates with local Ollama instance for AI-powered diagnosis.
"""
import requests
from typing import Optional


class OllamaClient:
    """
    Client for interacting with Ollama API.
    Sends prompts and receives AI-generated responses.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1"):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ollama API base URL (default: http://localhost:11434)
            model: Model to use for generation (default: llama3.1)
        """
        self.base_url = base_url
        self.model = model
        self.generate_url = f"{base_url}/api/generate"
    
    def generate(self, prompt: str, timeout: int = 30) -> Optional[str]:
        """
        Send a prompt to Ollama and get AI-generated response.
        
        Args:
            prompt: Text prompt to send to the AI
            timeout: Request timeout in seconds (default: 30)
        
        Returns:
            Generated text response, or None if error
        """
        try:
            # Prepare request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False  # Non-streaming response
            }
            
            # Send POST request to Ollama API
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=timeout
            )
            
            # Check if request was successful
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract generated text from response
                generated_text = response_data.get("response", "")
                return generated_text
            else:
                print(f"❌ Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"❌ Ollama request timeout after {timeout} seconds")
            return None
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Ollama at {self.base_url}")
            return None
        except Exception as e:
            print(f"❌ Error calling Ollama: {e}")
            return None
