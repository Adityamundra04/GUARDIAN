"""
AI service for Guardian.
Provides AI-powered diagnosis for Kubernetes incidents using Ollama.
"""
import sys
import os
from typing import Dict, Optional

# Add ai-engine to Python path for imports
ai_engine_path = os.path.join(os.path.dirname(__file__), '../../../ai-engine')
if ai_engine_path not in sys.path:
    sys.path.insert(0, ai_engine_path)

from ollama_client import OllamaClient


class AIService:
    """
    Service for AI-powered incident diagnosis.
    Analyzes Kubernetes issues and provides root cause and fix suggestions.
    """
    
    def __init__(self):
        """
        Initialize AI service with Ollama client.
        """
        self.ollama_client = OllamaClient(
            base_url="http://localhost:11434",
            model="llama3.1"
        )
    
    def build_diagnosis_prompt(self, issue: str) -> str:
        """
        Build a structured prompt for AI diagnosis.
        
        Args:
            issue: Description of the Kubernetes issue
        
        Returns:
            Formatted prompt for AI
        """
        prompt = f"""You are a Kubernetes expert.
Analyze the issue and provide:
1. Root cause
2. Fix

Issue: {issue}

Respond ONLY in this format:
Cause: <root cause explanation>
Fix: <step-by-step fix>"""
        
        return prompt
    
    def parse_ai_response(self, response: str) -> Dict[str, str]:
        """
        Parse AI response to extract cause and solution.
        
        Args:
            response: Raw AI-generated text
        
        Returns:
            Dictionary with 'cause' and 'solution' keys
        """
        # Default values if parsing fails
        cause = "Unknown"
        solution = "Manual investigation required"
        
        try:
            # Split response into lines
            lines = response.strip().split('\n')
            
            # Extract cause and fix
            for line in lines:
                line = line.strip()
                
                # Look for "Cause:" line
                if line.lower().startswith("cause:"):
                    cause = line.split(":", 1)[1].strip()
                
                # Look for "Fix:" line
                elif line.lower().startswith("fix:"):
                    solution = line.split(":", 1)[1].strip()
            
            # Handle multi-line responses
            if "cause:" in response.lower() and "fix:" in response.lower():
                # Find positions
                cause_start = response.lower().find("cause:")
                fix_start = response.lower().find("fix:")
                
                if cause_start != -1 and fix_start != -1:
                    # Extract cause (between "Cause:" and "Fix:")
                    cause_text = response[cause_start + 6:fix_start].strip()
                    if cause_text:
                        cause = cause_text
                    
                    # Extract fix (after "Fix:")
                    fix_text = response[fix_start + 4:].strip()
                    if fix_text:
                        solution = fix_text
        
        except Exception as e:
            print(f"❌ Error parsing AI response: {e}")
        
        return {
            "cause": cause,
            "solution": solution
        }
    
    def diagnose_issue(self, issue: str) -> Dict[str, str]:
        """
        Get AI-powered diagnosis for a Kubernetes issue.
        
        Args:
            issue: Description of the Kubernetes issue
        
        Returns:
            Dictionary with 'cause' and 'solution' keys
        """
        try:
            print(f"🤖 Requesting AI diagnosis for: {issue}")
            
            # Build prompt
            prompt = self.build_diagnosis_prompt(issue)
            
            # Call Ollama
            response = self.ollama_client.generate(prompt)
            
            if response:
                print(f"✅ AI response received")
                
                # Parse response
                diagnosis = self.parse_ai_response(response)
                
                print(f"📋 Cause: {diagnosis['cause'][:50]}...")
                print(f"🔧 Solution: {diagnosis['solution'][:50]}...")
                
                return diagnosis
            else:
                print(f"❌ AI diagnosis failed - using defaults")
                return {
                    "cause": "Unknown - AI service unavailable",
                    "solution": "Manual investigation required"
                }
        
        except Exception as e:
            print(f"❌ Error in AI diagnosis: {e}")
            return {
                "cause": "Unknown - AI error",
                "solution": "Manual investigation required"
            }
