"""
AI service for Guardian.
Provides AI-powered diagnosis for Kubernetes incidents using Ollama.
"""
import sys
import os
from typing import Dict, Union
from backend.app.core.logger import get_ai_logger

# Initialize logger
logger = get_ai_logger()

# Add ai-engine to Python path for imports
ai_engine_path = os.path.join(os.path.dirname(__file__), '../../../ai-engine')
if ai_engine_path not in sys.path:
    sys.path.insert(0, ai_engine_path)

from ai_engine.ollama_client import OllamaClient


class AIService:
    def __init__(self):
        self.ollama_client = OllamaClient(
            base_url="http://localhost:11434",
            model="llama3.1"
        )

    # -------------------------------
    # Prompt Builder (METRICS + LOGS AWARE)
    # -------------------------------
    def build_diagnosis_prompt(self, issue_context: Union[str, Dict[str, str]]) -> str:
        if isinstance(issue_context, dict):
            pod_name = issue_context.get('name', 'unknown')
            namespace = issue_context.get('namespace', 'unknown')
            error = issue_context.get('issue', 'unknown')
            
            # Extract metrics if available
            cpu_usage = issue_context.get('cpu_usage', 'N/A')
            memory_mb = issue_context.get('memory_mb', 'N/A')
            restart_count = issue_context.get('restart_count', 'N/A')
            
            # Extract logs if available
            logs = issue_context.get('logs', '')
            
            # Build context with metrics
            context = f"""Pod: {pod_name}
Namespace: {namespace}
Error: {error}
CPU Usage: {cpu_usage}
Memory Usage: {memory_mb}
Restart Count: {restart_count}"""
            
            # Add logs if available
            if logs and logs.strip():
                # Truncate logs if too long
                max_log_chars = 1500
                if len(logs) > max_log_chars:
                    logs = logs[-max_log_chars:]
                    logs = "...(truncated)\n" + logs
                
                context += f"\n\nRecent Container Logs:\n{logs}"
        else:
            context = f"Issue: {issue_context}"

        prompt = f"""You are a Kubernetes SRE with expertise in diagnosing production issues.

Analyze the issue using the provided information including metrics and logs.

Issue details:
{context}

Analysis Guidelines:
- PRIORITIZE log analysis - stack traces, errors, and exceptions are the most reliable indicators
- If logs contain error messages, stack traces, or missing dependencies, use those as primary evidence
- High CPU usage (>0.5 cores) may indicate CPU-intensive workload or runaway process
- High memory usage (>80% of limit) may indicate memory leak or OOM condition
- High restart count (>3) indicates unstable workload or configuration issue
- CrashLoopBackOff with high restarts suggests persistent startup failure
- Look for patterns in logs: connection errors, missing files, permission issues, dependency failures
- Consider metrics when determining root cause
- DO NOT assume unknown details
- If information is insufficient, say "Insufficient data"
- Be realistic and conservative
- Keep answer short and actionable

Respond ONLY:

Cause: <specific cause>
Fix: <specific fix>
"""

        return prompt

    # -------------------------------
    # Safe Parsing
    # -------------------------------
    def parse_ai_response(self, response: str) -> Dict[str, str]:
        cause = "Unknown"
        solution = "Manual investigation required"

        if not response or not response.strip():
            return {"cause": cause, "solution": solution}

        try:
            response_lower = response.lower()

            has_cause = "cause:" in response_lower
            has_fix = "fix:" in response_lower

            if has_cause and has_fix:
                cause_start = response_lower.find("cause:")
                fix_start = response_lower.find("fix:")

                if cause_start != -1 and fix_start != -1 and fix_start > cause_start:
                    cause_text = response[cause_start + 6:fix_start].strip()
                    cause_text = cause_text.replace('\n', ' ').replace('-', '').strip()

                    if len(cause_text) > 3:
                        cause = cause_text

                fix_text = response[fix_start + 4:].strip()
                fix_text = fix_text.replace('\n', ' ').replace('-', '').strip()

                if len(fix_text) > 3:
                    solution = fix_text

        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")

        return {
            "cause": cause,
            "solution": solution
        }

    # -------------------------------
    # Main Diagnosis Function (METRICS + LOGS AWARE)
    # -------------------------------
    def diagnose_issue(self, issue_context: Union[str, Dict[str, str]]) -> Dict[str, str]:
        try:
            # -------------------------------
            # Rule-Based Accurate Detection (🔥 IMPORTANT)
            # Enhanced with metrics and logs awareness
            # -------------------------------
            if isinstance(issue_context, dict):
                error = issue_context.get("issue", "")
                restart_count = issue_context.get("restart_count", "N/A")
                memory_mb = issue_context.get("memory_mb", "N/A")
                logs = issue_context.get("logs", "")

                if "CrashLoopBackOff" in error:
                    # Enhanced diagnosis with restart count
                    if restart_count != "N/A" and isinstance(restart_count, int) and restart_count > 5:
                        return {
                            "cause": f"Container repeatedly crashes after startup (CrashLoopBackOff) with {restart_count} restarts - indicates persistent failure",
                            "solution": "Check container logs using kubectl logs and verify application startup, entrypoint, and dependencies"
                        }
                    return {
                        "cause": "Container repeatedly crashes after startup (CrashLoopBackOff)",
                        "solution": "Check container logs using kubectl logs and verify application startup or entrypoint"
                    }

                if "ImagePullBackOff" in error:
                    return {
                        "cause": "Kubernetes cannot pull container image",
                        "solution": "Verify image name, registry access, and imagePullSecrets"
                    }

                if "restart" in error.lower():
                    # Enhanced diagnosis with restart count
                    if restart_count != "N/A" and isinstance(restart_count, int):
                        return {
                            "cause": f"Container is unstable with {restart_count} restarts - may indicate resource issues or application bugs",
                            "solution": "Check logs and resource limits (CPU/memory), verify dependencies, and review application health checks"
                        }
                    return {
                        "cause": "Container is unstable and restarting frequently",
                        "solution": "Check logs and resource limits (CPU/memory) and verify dependencies"
                    }

            # -------------------------------
            # AI fallback (for unknown cases) - now metrics + logs aware
            # -------------------------------
            if isinstance(issue_context, dict):
                log_msg = f"[{issue_context.get('namespace')}] {issue_context.get('name')} - {issue_context.get('issue')}"
                has_logs = bool(issue_context.get('logs', '').strip())
                log_indicator = " (with logs)" if has_logs else ""
            else:
                log_msg = str(issue_context)
                log_indicator = ""

            logger.info(f"Requesting AI diagnosis for: {log_msg}{log_indicator}")

            prompt = self.build_diagnosis_prompt(issue_context)

            response = self.ollama_client.generate(prompt, timeout=30)

            if not response or len(response) < 10:
                raise ValueError("Empty AI response")

            logger.info(f"AI response received ({len(response)} chars)")

            diagnosis = self.parse_ai_response(response)

            logger.info(f"Cause: {diagnosis['cause'][:80]}")
            logger.info(f"Solution: {diagnosis['solution'][:80]}")

            return diagnosis

        except Exception as e:
            logger.error(f"Error in AI diagnosis: {e}", exc_info=True)

            return {
                "cause": "Unknown - AI error",
                "solution": "Manual investigation required"
            }