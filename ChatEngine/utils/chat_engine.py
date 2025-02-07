import json
import time
import os

from openai import OpenAI

from .retriever import retrieve_documents, retrieve_weather
from .retriever_lists import tools
from .spinner import Spinner
from .tools import messages_log

class ChatEngine:
    '''
    ChatEngine class to handle the chat interaction with the AI model.
    Initial parameters:
    - base_url: The base URL of the OpenAI API.
    - api_key: The API key for the OpenAI API.
    - model: The model name to use for the chat interaction
    '''
    def __init__(self, base_url, api_key, model):
        with Spinner("Initializing profiles"):
            self.date = time.strftime("%Y-%m-%d", time.localtime())
            self.client = OpenAI(base_url=base_url, api_key=api_key)
            self.model = model
            self.messages = [{"role": "system", "content": "你是一个AI助手，语言风格有趣，可以带emoji表情，主要回答用户疑问。"}]
            self.messages.append({"role": "assistant", "content": f"today date: {self.date}"})

            history_file = "ChatEngine/data/history.json"
            # check history.json file
            try:
                with open(history_file, "r") as f:
                    # if history.json exists but empty
                    if os.stat(history_file).st_size == 0:
                        self.history = []
                        welcome_message = "你好，初次见面！"
                    elif os.stat(history_file).st_size >= 10:
                        # read last 10 history messages, 5 pairs of user input and response
                        self.history = json.load(f)[-10:]
                        welcome_message = "你好，欢迎回来！"
                    else:
                        # read last few history messages
                        self.history = json.load(f)
                        if len(self.history) == 0:
                            welcome_message = "你好，初次见面！"
                        else:
                            welcome_message = "你好，欢迎回来！"
            except FileNotFoundError:
                self.history = []
                welcome_message = "你好，初次见面！"

            # print(self.history)

        print("Assistant>>")
        for char in welcome_message:
            print(char, end="", flush=True)
            time.sleep(0.05)

        print("\n(Type '/bye' to exit)")

    def generate_response(self, query):
        self.messages.extend(self.history)
        messages = self.messages
        messages.append({"role": "user", "content": query})

        searchmessages = [
            {"role": "system", "content": f"你是一个搜索引擎, date of today：{self.date}"}, 
            {"role": "user", "content": query}
        ]
        print("\nAssistant>>", end=" ", flush=True)
        try:
            with Spinner("Thinking..."):
                response = self.client.chat.completions.create(
                        model=self.model,
                        messages=searchmessages,
                        temperature=0.8,
                        max_tokens=1024,
                        tools=tools,
                )
                if response.choices[0].message.tool_calls:
                    # Handle all tool calls
                    tool_calls = response.choices[0].message.tool_calls
                    for tool_call in tool_calls:
                        try:
                            result = {"status": "error", "content": "None"}
                            args = json.loads(tool_call.function.arguments)
                            
                            # if tool_call.function.name == "retrieve_documents":
                            #     result = retrieve_documents(args["search_query"])
                            # elif tool_call.function.name == "retrieve_weather":
                            #     result = retrieve_weather(args["city"], args["date"])

                            result = globals()[tool_call.function.name](**args)

                            messages.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "role": "tool",
                                        "name": tool_call.function.name,
                                        "content": json.dumps(result['content'], ensure_ascii=False)
                                    }
                            )
                            # Print the ontent in a formatted way
                                
                            # import shutil
                            # terminal_width = shutil.get_terminal_size().columns
                            # print("\n" + "=" * terminal_width)
                            # print("-" * terminal_width)
                            # print(result["content"])
                            # print("=" * terminal_width + "\n")

                        except Exception as e:
                            print(
                                "An error occurred while processing your request. Please try again later.\n"
                                f"Error details: {str(e)}\n"
                            )
                            exit(1)

                stream_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages_log(messages, "stream_response"), # if don't need log, use messages
                        temperature=0.8,
                        max_tokens=4096,
                        frequency_penalty=0.8,
                        presence_penalty=0.5,
                        top_p=0.95,
                        stream=True
                )
            
            # Stream the post-tool-call response
            think_content = ""
            dialog_content = ""

            for chunk in stream_response:
                content = chunk.choices[0].delta.content
                if content:
                    if not think_content.endswith("</think>"):
                            print(content, end="", flush=True)
                            think_content += content
                    else:
                        content = chunk.choices[0].delta.content
                        print(content, end="", flush=True)
                        dialog_content += content
            print()  # New line after streaming completes

            self.history.append(
                {
                    "role": "user",
                    "content": query
                }
            )
            self.history.append(
                {
                    "role": "assistant",
                    "content": think_content + dialog_content
                }
            )

            # Save the chat history to history.json
            with open("ChatEngine/data/history.json", "w") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(
                "An error occurred while processing your request. Please try again later.\n"
                f"Error details: {str(e)}\n"
            )
            exit(1)

        
