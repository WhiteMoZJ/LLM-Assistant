import json
import time
import os

from openai import OpenAI

from .retriever import retrieve_documents, retrieve_weather
from .retriever import tools
from .spinner import Spinner
from .tools import sovle_response

class ChatEngine:
    '''
    ChatEngine class to handle the chat interaction with the AI model.
    Initial parameters:
    - base_url: The base URL of the OpenAI API.
    - model: The model name to use for the chat interaction
    '''
    def __init__(self, base_url):
        # check the connection to the OpenAI API
        self.api_key = ""
        if base_url == "http://localhost:1234/v1":
            self.api_key = "lm-studio"
        elif base_url == "http://localhost:8080/v1":
            self.api_key = "llama.cpp"
        self.client = OpenAI(base_url=base_url, api_key=self.api_key)

        with Spinner("Initializing profiles"):
            self.date = time.strftime("%Y-%m-%d", time.localtime())
            self.model = "deepseek-r1-distill-llama-8b"
            self.messages = [{"role": "system", "content": "你是一个AI助手，语言风格有趣，可以带emoji表情，主要回答用户疑问。"}]
            self.messages.append({"role": "assistant", "content": f"today date: {self.date}"})

            if os.path.exists("ChatEngine/.data") == False:
                os.mkdir("ChatEngine/.data")

            history_file = "ChatEngine/.data/history.json"
            # check history.json file
            try:
                with open(history_file, "r") as f:
                    # if history.json exists but empty
                    if os.stat(history_file).st_size == 0:
                        self.history = []
                        welcome_message = "你好，初次见面！"
                    elif os.stat(history_file).st_size >= 20:
                        # read last 20 history messages, 10 pairs of user input and response
                        self.history = json.load(f)[-20:]
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

        print("Assistant >>")
        for char in welcome_message:
            print(char, end="", flush=True)
            time.sleep(0.05)

        print("\n(Type '/' or '/help' for help, '/bye' to exit)")

    def generate_response(self, query):
        self.messages.extend(self.history)
        messages = self.messages
        messages.append({"role": "user", "content": query})

        if self.api_key == "llama.cpp":
            searchmessages = [
                {"role": "system", 
                "content": (
                    "You are an AI assistant that, output a JSON object containing a 'tool_call' field with the function call details. "
                    "Do not include any internal thinking or explanations—just output the tool_call JSON like"
                    "\"tool_calls\": [{\"type\": \"function\",\"function\": {\"name\": \"?\",\"arguments\": {}\"}}"
                    "It could be multi times to call different functions."
                )}, 
                {"role": "assistant", "content": f"The current date is {self.date}"},
                {"role": "user", "content": query}
            ]
        else:
            searchmessages = [
                {"role": "system", "content": f"You are a AI assistant. "}, 
                {"role": "assistant", "content": f"The current date is {self.date}"},
                {"role": "user", "content": query}
            ]

        print("\nAssistant>>", end=" ", flush=True)
        try:
            with Spinner("Thinking..."):
                response = self.client.chat.completions.create(
                        model=self.model,
                        messages=searchmessages,
                        temperature=0.5,
                        max_tokens=512,
                        tools=tools,
                        tool_choice="auto"
                )
                if self.api_key == "llama.cpp":
                    sovle_response(response)

                if response.choices[0].message.tool_calls:
                    # Handle all tool calls
                    for tool_call in response.choices[0].message.tool_calls:
                        if not tool_call.function.name in [tool['function']['name'] for tool in tools]:
                            continue
                        result = {"status": "error", "content": "None"}
                        try:
                            args = json.loads(tool_call.function.arguments)

                            result = globals()[tool_call.function.name](**args)

                            messages.append(
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call.id,
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

                stream_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
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
                    if not think_content.endswith("</think>\n\n"):
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
                    "content": dialog_content
                }
            )

            # Save the chat history to history.json
            with open("ChatEngine/.data/history.json", "w") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(
                "An error occurred while processing your request. Please try again later.\n"
                f"Error details: {str(e)}"
            )

    # get history
    def get_history(self):
        print("\nChat History:")
        print("\n".join([f"{item['role']}>> {item['content']}" for item in self.history]))
    
    # reset history
    def reset_history(self):
        self.history = []
        with open("ChatEngine/.data/history.json", "w") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
