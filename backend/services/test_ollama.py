import requests

def ask_llm(issue):
    prompt = f"""
You are a strict DevOps agent.

Issue: {issue}

The system runs a Python service:
service/service.py

Rules:
- DO NOT explain
- DO NOT give multiple commands
- DO NOT mention Linux/Windows differences
- ONLY return ONE command

Output format EXACTLY:
COMMAND: <single command>
"""

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False
        }
    )

    return res.json()["response"]


response = ask_llm("Service is down")

command = response.split("COMMAND:")[-1].strip()

print("AI Command:", command)