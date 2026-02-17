# Part 1: API Basics (Using OpenAI API)

"""
Write a Python script that demonstrates basic API interaction with your chosen provider:
    1. Create a function query_llm(prompt, **kwargs) that sends a prompt to your LLM and returns the response text. Include parameters for temperature and max_tokens.
    2. Implement proper error handling for common issues (connection errors, rate limits, authentication failures, timeouts).
    3. Add a simple retry mechanism with exponential backoff for transient failures.
    4. Write a main() function that demonstrates your query function with at least 3 different prompts and prints the responses.
"""

import os
import time
import requests

API_KEY = os.environ.get("OPENAI_API_KEY", "")

def query_llm(prompt, temperature=0.7, max_tokens=4098, max_retries=3):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}", # Because of this, run `export OPENAI_API_KEY='your-key-here'` in your terminal before running the script.
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    # Retry mechanism with exponential backoff for transient failures
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as http_err:
            status = http_err.response.status_code if http_err.response else None
            if status == 401:
                print(f"Authentication error: {http_err}")
                return None
            elif status == 429:
                wait = 2 ** attempt
                print(f"Rate limited. Retrying in {wait}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
            else:
                print(f"HTTP error occurred: {http_err}")
                return None
        except requests.exceptions.ConnectionError as conn_err:
            wait = 2 ** attempt
            print(f"Connection error. Retrying in {wait}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait)
        except requests.exceptions.Timeout as timeout_err:
            wait = 2 ** attempt
            print(f"Timeout. Retrying in {wait}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait)
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return None

    print("Max retries exceeded.")
    return None

def main():
    if not API_KEY:
        print("Error: Set OPENAI_API_KEY environment variable before running.")
        print("  export OPENAI_API_KEY='your-key-here'")
        return

    prompts = [
        "What is the capital of France?",
        "Explain Singular Value Decomposition in simple terms.",
        "Write a short poem about the ocean."
    ]

    for prompt in prompts:
        response = query_llm(prompt)
        if response:
            print(f"Prompt: {prompt}\nResponse: {response}\n")
        else:
            print(f"Failed to get a response for prompt: {prompt}\n")

if __name__ == "__main__":
    main()


# line