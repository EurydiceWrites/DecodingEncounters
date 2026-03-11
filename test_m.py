import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

prompt = """You are a precise data extraction engine.
Extract EVERY SINGLE motif event specifically for Cases 001 through 005.

RAW TEXT:
001. Bob [22] October 1950 / USA
E200 Bob saw a ship.
M119 Bob felt sad.

002. Alice [33]
B350 Alice was abducted.
"""

print("Calling API...")
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0
        )
    )
    print("Response received!")
    print(response.text)
except Exception as e:
    import traceback
    traceback.print_exc()
