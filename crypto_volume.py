import requests
import openai
import json
import os


openai.api_key = os.environ["OPENAI_API_KEY"]
rapid_key = os.environ["RAPID_KEY"]

user_prompt = "What is the 24hr volume of Bitcoin compared to the total 24hr volume of the crypto currency market?"

functions=[
        {
            "name": "bitcoin_24hr_volume",
            "description": "Bitcoin volume in last 24hrs",
            "parameters": {
                "type": "object",
                "properties": {
                    "24hVolume": {
                        "type": "string",
                        "description": "The 24 hour volume of Bitcoin which is referred to as 24hVolume in the api response.",
                    },
                },
                "required": ["24hVolume"],
            },
        },
        {
            "name": "global_24hr_volume",
            "description": "Compare the global 24hr volume in the crypto market to the 24hr volume of Bitcoin",
            "parameters": {
                "type": "object",
                "properties": {
                    "24hVolume": {
                        "type": "string",
                        "description": "The total 24 hour volume of the crpyto market which is referred to as total24hVolume in the api response.",
                    },
                },
                "required": ["total24hVolume"],
            },
        }
]

def bitcoin_24hr_volume():
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd"

    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h"}

    headers = {
        "X-RapidAPI-Key": rapid_key,
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()

def global_24hr_volume():
    url = "https://coinranking1.p.rapidapi.com/stats"

    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl"}

    headers = {
        "X-RapidAPI-Key": rapid_key,
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def crypto_function_calling(resp):
    function_call = resp["choices"][0]["message"]["function_call"]
    function_name = function_call["name"]
    if function_name == "bitcoin_24hr_volume":
        return bitcoin_24hr_volume()
    elif function_name == "global_24hr_volume":
        return global_24hr_volume()

def continue_functions(user_prompt):
    messages = [{"role": "user", "content": user_prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
)

    print(response)

    while response["choices"][0]["finish_reason"] == "function_call":
        func_resp = crypto_function_calling(response)
        messages.append({
            "role": "function",
            "name": response["choices"][0]["message"]["function_call"]["name"],
            "content": json.dumps(func_resp)
        })

        print("messages: ", messages) 

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",
)

        print("response: ", response) 
    else:
        print(response["choices"][0]["message"]["content"])

continue_functions(user_prompt)
