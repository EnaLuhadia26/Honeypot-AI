import random
import time

class DecoyGenerator:
    """
    Template-based fake responses for honeypot.
    """
    def __init__(self, mode="template"):
        self.templates = [
            "Server is initializing... please wait.",
            "403 Forbidden. You do not have permission to access this resource.",
            "Error: database connection failed; retrying.",
            "Welcome, admin. Last login: 2025-01-01 12:00:00",
            "Service temporarily unavailable. Please try again later.",
            "Invalid credentials. 2 attempts remaining.",
            "SSH: connection refused. Check service status."
        ]

    def generate_response(self, event):
        return self._template_response(event)

    def _template_response(self, event):
        t = random.choice(self.templates)
        if random.random() < 0.3:
            t = f"{t} (session={int(time.time())%10000})"
        return t
