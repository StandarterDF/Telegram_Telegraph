from openai import OpenAI
import json
import math

# Connect to LM Studio
client = OpenAI(base_url="http://192.168.0.124:1234/v1", api_key="qwen2.5-coder-3b-instruct")

# Tell the AI about our function
tools = [
    {
        "type": "function",
        "function": {
            "name": "mult_numbers",
            "description": "Перемножение двух чисел",
            "parameters": {
                "type": "object",
                "properties": {
                    "number1": {
                        "type": "number",
                        "description": "Первое число"
                    },
                    "number2": {
                        "type": "number",
                        "description": "Второе число"
                    }
                },
                "required": ["number1", "number2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "root",
            "description": "Квадратный корень из заданного числа",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {
                        "type": "number",
                        "description": "Число из которого нужно извлечь корень"
                    }
                },
                "required": ["number"]
            }
        }
    }
]


while True:
    # Ask the AI to use our function
    prompt = input("Enter prompt: ")
    answer = ""
    trys = 0
    while True:
        if trys >= 5: break
        response = client.chat.completions.create(
            model="qwen2.5-coder-3b-instruct",
            messages=[{"role": "user", "content": prompt}],
            tools=tools,
            temperature=0
        )
        tool_call = response.choices[0].message.content
        try:
            json_decode = json.loads(tool_call[8:-3])
            break
        except:
            trys += 1
            continue
    try:
        json_decode = json.loads(tool_call[8:-3])
        if json_decode["name"] == "root":
            print("Answer: ", math.sqrt(float(json_decode["arguments"]["number"])))
        elif json_decode["name"] == "mult_numbers":
            print("Answer: ", float(json_decode["arguments"]["number1"]) * float(json_decode["arguments"]["number2"]))
        else:
            print("Answer: ", tool_call[8:-3])
    except:
        print("Answer: ", tool_call)
