import requests
import json

def get_chatgpt_response(prompt):
    url = "https://openai-chatgpt-35-instant-access.herokuapp.com/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {str(e)}")
        return None

# Example usage
prompt = "Tell me about the history of Python programming language."
response = get_chatgpt_response(prompt)

if response:
    print("ChatGPT Response:")
    print(response)
else:
    print("Failed to retrieve ChatGPT response.")