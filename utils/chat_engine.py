import shutil
import json

from openai import OpenAI

from .search_request import retrieve_documents
from .search_tool import ONLINE_SEARCH_TOOL
from .spinner import Spinner

class ChatEngine:
    def __init__(self):
        # presets = os.listdir('presets')
        # preset = json.loads(open("presets/" + presets[0], "r").read())
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        self.model = "deepseek-r1-distill-llama-8b"
        # self.messages= [{"role": "system", "content": preset['operation']['fields'][5]['value']}]
        self.messages= [{"role": "system", "content": "你是一个AI管家，语言风格有趣，可以带emoji表情，主要回答用户疑问，必要时总结用户输入文本内容，如果文本中出现转义字符错误，不予理会，不需要向用户解释你的功能"}]

        print(
            "Assistant: "
            "你好，欢迎回来！"
        )
        print("(Type 'quit' to exit)")

    def generate_response(self, query):
        self.messages.append({"role": "user", "content": query})
        print("\nAssistant:", end=" ", flush=True)
        with Spinner("Thinking..."):
            response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    temperature=0.7,
                    max_tokens=512,
                    tools=[ONLINE_SEARCH_TOOL],
            )

            if response.choices[0].message.tool_calls:
                # Handle all tool calls
                tool_calls = response.choices[0].message.tool_calls
                # Add all tool calls to messages
                self.messages.append(
                        {
                            "role": "assistant",
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": tool_call.type,
                                    "function": tool_call.function,
                                }
                                for tool_call in tool_calls
                            ],
                        }
                )

                for tool_call in tool_calls:
                    try:
                        args = json.loads(tool_call.function.arguments)
                        # Retrieve documents (context) from the search engine
                        result = retrieve_documents(args["search_query"])

                        # Print the ontent in a formatted way
                        # if result["status"] == "success":
                        #     terminal_width = shutil.get_terminal_size().columns
                        #     print("\n" + "=" * terminal_width)
                        #     print("-" * terminal_width)
                        #     print(result["content"])
                        #     print("=" * terminal_width + "\n")

                        # self.messages.append(
                        #         {
                        #             "role": "tool",
                        #             "content": json.dumps(result),
                        #             "tool_call_id": tool_call.id,
                        #         }
                        # )
                        self.messages.append(
                                {
                                    "role": "assistant",
                                    "content": f"Context:\n{result['content']}\n\nQuestion: {query}\n"
                                }
                        )
                    except Exception as e:
                        continue

            stream_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    temperature=0.8,
                    max_tokens=4096,
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
                    print(content, end="", flush=True)
                    dialog_content += content
        print()  # New line after streaming completes
        self.messages.append(
            {
                "role": "assistant",
                "content": dialog_content,
            }
        )
