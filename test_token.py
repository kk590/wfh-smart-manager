"""Quick test to verify the GitHub token works."""
import requests

token = "YOUR_GITHUB_TOKEN_HERE"
r = requests.post(
    "https://models.github.ai/inference/chat/completions",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "Say hi"}], "max_tokens": 5},
    timeout=30,
)
print(f"Status: {r.status_code}")
print(r.text[:300])
