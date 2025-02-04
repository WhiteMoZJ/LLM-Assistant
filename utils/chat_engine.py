import json
import shutil

from openai import OpenAI

from .retriever import retrieve_documents
from .retriever_lists import ONLINE_SEARCH_TOOL
from .spinner import Spinner

class ChatEngine:
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        self.model = "deepseek-r1-distill-llama-8b"
        self.messages= [{"role": "system", "content": "你是一个AI助手，语言风格有趣，可以带emoji表情，主要回答用户疑问。"}]

        print(
            "Assistant: "
            "你好，欢迎回来！"
        )
        print("(Type 'quit' to exit)")

    def generate_response(self, query):
        messages = self.messages
        searchmessages = [{"role": "system", "content": "你是一个AI助手"}, {"role": "user", "content": query}]
        print("\nAssistant:", end=" ", flush=True)
        with Spinner("Thinking..."):
            response = self.client.chat.completions.create(
                    model=self.model,
                    messages=searchmessages,
                    temperature=0.7,
                    max_tokens=512,
                    tools=[ONLINE_SEARCH_TOOL],
            )

            if response.choices[0].message.tool_calls:
                # Handle all tool calls
                tool_calls = response.choices[0].message.tool_calls
                # [ChatCompletionMessageToolCall(id='536605354', 
                #                                function=Function(arguments='{"search_query":"XXX"}', 
                #                                name='retrieve_documents'), 
                #                                type='function')

                # Add all tool calls to messages
                messages.append(
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

                        if result["status"] == "success":
                            messages.append(
                                    {
                                        "role": "assistant",
                                        "content": result["content"],
                                        "tool_call_id": tool_call.id,
                                    }
                            )
                            # Print the ontent in a formatted way
                            # terminal_width = shutil.get_terminal_size().columns
                            # print("\n" + "=" * terminal_width)
                            # print("-" * terminal_width)
                            # print(result["content"])
                            # print("=" * terminal_width + "\n")

                        else:
                            messages.append(
                                    {
                                        "role": "assistant",
                                        "content": "网络错误，请稍后再试。",
                                        "tool_call_id": tool_call.id,
                                    }
                            )
                    except Exception as e:
                        continue
            else:
                messages = self.messages
            messages.append({"role": "user", "content": query})

            stream_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
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
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    dialog_content += content
        print()  # New line after streaming completes
        self.messages.append(
            {
                "role": "assistant",
                "content": dialog_content,
            }
        )
