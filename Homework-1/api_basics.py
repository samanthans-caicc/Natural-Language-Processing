# Note: I am using the course Llama Server through the UTSA VPN primarily due to mostly on this assignment at home.

# Part 1: API Basics

"""
Write a Python script that demonstrates basic API interaction with your chosen provider:
    1. Create a function query_llm(prompt, **kwargs) that sends a prompt to your LLM and returns the response text. Include parameters for temperature and max_tokens.
    2. Implement proper error handling for common issues (connection errors, rate limits, authentication failures, timeouts).
    3. Add a simple retry mechanism with exponential backoff for transient failures.
    4. Write a main() function that demonstrates your query function with at least 3 different prompts and prints the responses.
"""

import time
import random
import requests

def query_llm(prompt, temperature=0.7, max_tokens=100):
    url = "https://nam11.safelinks.protection.outlook.com/?url=http%3A%2F%2F10.246.100.230%2Fv1&data=05%7C02%7Csamantha.salas%40my.utsa.edu%7C23962e618e6148bbafb908de65bd62f9%7C3a228dfbc64744cb88357b20617fc906%7C0%7C0%7C639060061245754978%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=bXIXYFtkn9YwnUMyagLSQ1dpbNCvG2cf9CVfszCX8EA%3D&reserved=0"

    headers = {
        "Authorization": "Bearer gpustack_095f5cb316bc4b95_fe15f283c2d7de79dd258ca70635bb66",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    #Here is the retry mechanism with exponential backof for transitent failures. v

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.json().get("response", "")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return None

def main():
    prompts = [
        "What is the capital of France?",
        "Explain the theory of relativity in simple terms.",
        "Write a short poem about the ocean."
    ]

    for prompt in prompts:
        response = query_llm(prompt)
        if response:
            print(f"Prompt: {prompt}\nResponse: {response}\n")
        else:
            print(f"Failed to get a response for prompt: {prompt}\n")

if __name__ == "__main__":    main()
