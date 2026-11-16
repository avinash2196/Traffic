import os
from pathlib import Path

print("Working directory:", os.getcwd())

env_path = Path(__file__).resolve().parent / '.env'
print(f"Looking for .env at: {env_path}")
print(f".env exists: {env_path.exists()}")

if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key, value = parts
                    os.environ[key.strip()] = value.strip()

print(f"GATEWAY_TOKEN: {os.getenv('GATEWAY_TOKEN', 'NOT SET')}")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'NOT SET')[:20]}...")
