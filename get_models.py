import os
import requests
import json
import time

env_path = ".env"
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"\'')

token = os.environ.get("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

CACHE_FILE = ".models_cache.json"
CACHE_EXPIRY_SEC = 86400  # 24 hours

def get_models():
    # Check cache first to reduce latency
    if os.path.exists(CACHE_FILE):
        if time.time() - os.path.getmtime(CACHE_FILE) < CACHE_EXPIRY_SEC:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
    
    # If not in cache or expired, fetch from network
    print("Fetching models from network (this might take a moment)...")
    resp = requests.get("https://models.github.ai/catalog/models", headers=headers, timeout=10)
    if resp.status_code == 200:
        models automodel = resp.json()
        # Save to cache
        with open(CACHE_FILE, "w") as f:
            json.dump(models, f)
        return models
    else:
        print("Failed to fetch models:", resp.status_code, resp.text)
        return []

try:
    models = get_models()
    if models:
        print("AVAILABLE MISTRAL MODELS:")
        for m in models:
            if "mistral" in m.get("id", "").lower():
                print(m.get("id"))
except Exception as e:
    print("Error:", e)
