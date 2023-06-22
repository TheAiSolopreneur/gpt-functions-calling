import openai
import json
import os

openai.api_key = os.environ["OPENAI_API_KEY"]


user_prompt = "What is the capital of Italy?"
user_prompt2 = "How do I write an email to my boss about taking some PTO?"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": user_prompt2}],
    functions=[
        {
            "name": "write_varied_email",
            "description": "Write the email to my boss with different tones",
            "parameters": {
                "type": "object",
                "properties": {
                    "friendly": {
                        "type": "string",
                        "description": "A friendly and casual version of the PTO email.",
                    },
                    "professional": {
                        "type": "string",
                        "description": "A professional and serious version of the PTO email.",
                    },
                    "witty": {
                        "type": "string",
                        "description": "A witty version of the PTO email.",
                    },
                       
                },
                "required": ["friendly","professional","witty"],
            },
        }
    ],
    function_call= {"name": "write_varied_email"}
)

message = response["choices"][0]["message"]
email_options = message.to_dict()['function_call']['arguments']
emails = json.loads(email_options)

# print(message)

print(f"Friendly -> {emails['friendly']} \n")
print(f"Professional -> {emails['professional']} \n")
print(f"Witty -> {emails['witty']} \n")
