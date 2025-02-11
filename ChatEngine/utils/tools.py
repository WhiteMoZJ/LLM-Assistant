import json
import time
import re
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
from typing import List
from xpinyin import Pinyin

def messages_log(message:dict, response: str) -> dict:
    log_message = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "response": response,
        "message": message
    }

    log_file = f"ChatEngine/.log/log-{time.strftime('%Y-%m-%d', time.localtime())}.json"
    with open(log_file, "a") as f:
        json.dump(log_message, f, ensure_ascii=False, indent=4)
    return message

def sovle_response(response:ChatCompletion):
    '''
    This function is to solve tool calls of the response from the model. 
    Designed for llama.cpp\n
    The original response from the model contains tool calls in the content\n
    The tool calls are in the format of ```json ... ```\n
    The function will extract the tool calls and store them in the response object
    '''
    try:
        content = response.choices[0].message.content
        match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if match:
            json_content = match.group(1)
            tool_calls_data: List[dict] = json.loads(json_content)["tool_calls"]
            for item in tool_calls_data:
                if isinstance(item["function"]["arguments"], dict):
                    item["id"] = str(time.time()).replace(".", "")[-9:]
                    item["function"]["arguments"] = json.dumps(item["function"]["arguments"], ensure_ascii=False)
            # print(tool_calls_data)
            response.choices[0].message.tool_calls = [ChatCompletionMessageToolCall(**item) for item in tool_calls_data]

        match = re.search(r'<think>\s*(.*?)\s*</think>', content, re.DOTALL)
        if match:
            response.choices[0].message.content = "<think>" + match.group(1) + "</think>"
    except Exception as e:
        print(f"An error occurred: {e}")
    # return response

def get_pinyin(name):
    s = Pinyin().get_pinyin(name).split('-')
    result = ''
    for i in range(0,len(s)):
        result = result+s[i].capitalize()
    return result