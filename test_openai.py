#!/usr/bin/env python
"""Test OpenAI API directly with the provided key."""
import os
import json
from openai import OpenAI

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("ERROR: OPENAI_API_KEY not set")
    exit(1)

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a traffic violation detector."},
            {"role": "user", "content": "Is this a traffic violation?"}
        ],
        temperature=1,
        max_tokens=500,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "test_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"},
                        "confidence": {"type": "number"}
                    },
                    "required": ["result"]
                }
            }
        }
    )
    
    print("OpenAI API is working!")
    print(f"Model: {response.model}")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"OpenAI API ERROR: {e}")
