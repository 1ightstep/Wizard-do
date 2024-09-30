import requests
import json


class AI:
    def __init__(self):
        self.url = "https://api.arliai.com/v1/chat/completions"
        self.ARLIAI_API_KEY = "<API KEY>"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.ARLIAI_API_KEY}"
        }

    def filter_list(self, prompt, list):
        payload = json.dumps({
            "model": "Mistral-Nemo-12B-Instruct-2407",
            "messages": [
                {"role": "system", "content": "ONLY RETURN A PYTHON LIST WITH NO COMMENTS!"},
                {"role": "user", "content": f"ONLY RETURN A PYTHON LIST WITH NO COMMENTS! {prompt}; USE THIS LIST: {list}"},
            ],
            "repetition_penalty": 1.1,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_tokens": 1024,
            "stream": False
        })

        response = requests.post(self.url, headers=self.headers, data=payload)
        if response.status_code == 200:
            result = response.json()
        return result['choices'][0]['message']['content']
