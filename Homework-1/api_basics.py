# Write a Python script that demonstrates basic API interaction with your chosen provider:
#    1. Create a function query_llm(prompt, **kwargs) that sends a prompt to your LLM and returns the response text. Include parameters for temperature and max_tokens.
#   2. Implement proper error handling for common issues (connection errors, rate limits, authentication failures, timeouts).
#   3. Add a simple retry mechanism with exponential backoff for transient failures.
#   4. Write a main() function that demonstrates your query function with at least 3 different prompts and prints the responses.

import time
import random
import requests

def query_llm(prompt, temperature=0.7, max_tokens=100):
    url = "https://api.example.com/llm"  # Replace with your LLM API endpoint
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API key
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens    }
    try:    
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("text", "")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

def main():
    prompts = [
        "What is the capital of France?",
        "Explain the theory of relativity in simple terms.",
        "Write a short poem about the ocean."
    ]
    
    for prompt in prompts:
        print(f"Prompt: {prompt}")
        response = query_llm(prompt)
        print(f"Response: {response}\n")
        time.sleep(random.uniform(1, 3))  # Simulate delay between requests
        
if __name__ == "__main__":    main()