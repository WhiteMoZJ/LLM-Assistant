from utils.chat_engine import ChatEngine

def chat_loop():
    chatEngine = ChatEngine()
    print(
            "Assistant: "
            "你好，欢迎回来！"
    )
    print("(Type 'quit' to exit)")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "quit":
            break
        print("\nAssistant:", end=" ", flush=True)
        chatEngine.generate_response(user_input)


if __name__ == "__main__":
    chat_loop()