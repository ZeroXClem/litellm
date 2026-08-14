import os
import litellm
from litellm import completion

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = ""

# Define the messages and functions
messages = [
    {"role": "user", "content": "What is the weather like in Boston?"}
]

def get_current_weather(location):
    if location == "Boston, MA":
        return "12F"

functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
]

# Call the gpt-3.5-turbo-0613 model to decide what function to call
response = completion(model="gpt-3.5-turbo-0613", messages=messages, functions=functions)
print(response)

# Parse the GPT 3.5 response
function_call_data = response["choices"][0]["message"]["function_call"]
function_name = function_call_data['name']
function_args = json.loads(function_call_data['arguments'])

# Call the get_current_weather() function
if function_name == "get_current_weather":
    result = get_current_weather(**function_args)
    print(result)

# Send the response from get_current_weather back to the model to summarize
messages = [
    {"role": "user", "content": "What is the weather like in Boston?"},
    {"role": "assistant", "content": None, "function_call": {"name": "get_current_weather", "arguments": "{ \"location\": \"Boston, MA\"}"}},
    {"role": "function", "name": "get_current_weather", "content": result}
]
response = completion(model="gpt-3.5-turbo-0613", messages=messages, functions=functions)
print(response)
