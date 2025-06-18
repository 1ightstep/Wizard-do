import json

import time

import requests


class AI:
    def __init__(self):
        self.url = "https://api.arliai.com/v1/chat/completions"
        self.ARLIAI_API_KEY = ""
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.ARLIAI_API_KEY}"
        }

    def filter_list(self, prompt, lst):
        SYSTEM_PROMPT = """
        YOU'RE A PERSONAL ASSISTANCE THAT MANAGES AN TASK APP'S FUNCTION.
        EVERYTIME YOU'RE GIVEN A PYTHON LIST OF TASKS CONTAINING DICTIONARIES.
        REORGANIZE THEM BASED ON THE PROMPT.
        IF YOU'RE TOLD TO ADD MORE TASKS TO THE LIST, PLEASE DO SO BUT FOLLOW THIS FORMAT:
        {"to_create": True, "task_tag": <task_tag>, task_name": "<TASK_NAME>", "task_date": "month/day/year", "task_time": "hour:minute; military time"}
        *THERE SHOULD NOT BE A LEADING ZERO IN ANY NUMBER.
        *THE task_tag OF EACH OBJECT/TASK SHOULD BE EITHER "Goal", "Urgent", "Important", "Medium", "Low"!
        *ALWAYS RETURN A PYTHON LIST!
        *MAKE SURE PYTHON CAN PARSE IT WITHOUT ERROR!
        *DO NOT INCLUDE ANY COMMENTS
        *MAKE SURE EVERYTHING IS SYNTACTICALLY CORRECT! 
        *MAKE SURE EVERY STRING IS IN DOUBLE QUOTES!
        *DO NOT MODIFY THE ORIGINAL TASKS, JUST REORGANIZE THEM BASED ON THE PROMPT!
        *MAKE SURE TO MODIFY task_date and task_time FOR NEW TASKS!
        *MAKE SURE THE TASKS YOU ARE ADD ARE RELEVANT AND SYNONYMOUS WITH THE USER'S LIFESTYLE AND TASKS
        *MAKE SURE TIME IS FORMATTED CORRECTLY! ONLY MILITARY TIME, NO WORDS LIKE MORNING, AFTERNOON, OR EVENING.\n
        *MAKE SURE THE YEAR IS A FOUR-DIGIT NUMBER.
        """ + f"*USE TODAY'S DATE, TIME, AND *DAY* : {time.strftime("%A, %D %B %Y %H:%M:%S", time.localtime())}"
        task_name_list = list(
            {"to_create": False, "task_tag": task["task_tag"], "task_name": task["task_name"],
             "task_date": task["task_date"], "task_time": task["task_time"]}
            for task in lst
        )
        payload = json.dumps({
            "model": "Mistral-Nemo-12B-Instruct-2407",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"PROMPT: {prompt}; LIST: {task_name_list}"},
            ],
            "repetition_penalty": 1.1,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_tokens": 2048,
            "stream": False
        })
        try:
            response = requests.post(self.url, headers=self.headers, data=payload)
            if response.status_code == 200:
                result = response.json()
            result = eval(result['choices'][0]['message']['content'])
        except Exception as e:
            return {'status': 'error', 'list': []}
        return {'status': 'success', 'list': result}
