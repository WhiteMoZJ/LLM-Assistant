from utils.chat_engine import ChatEngine

def chat_loop():
    chatEngine = ChatEngine("http://localhost:1234/v1", "lm-studio", "deepseek-r1-distill-llama-8b")
    while True:
        user_input = input("\nYou>>").strip()
        if user_input.lower() == "/bye":
            break
        print("\nAssistant>>", end=" ", flush=True)
        chatEngine.generate_response(user_input)


if __name__ == "__main__":
    chat_loop()