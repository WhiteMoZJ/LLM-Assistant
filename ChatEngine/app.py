from utils.chat_engine import ChatEngine

def chat_loop():
    chatEngine = ChatEngine("http://localhost:8080/v1")
    '''
    In this specific instance, the `base_url` is set to `"http://localhost:8080/v1"`, 
    which points to a locally hosted API endpoint
    '''
    while True:
        user_input = input("\nYou>>").strip()
        if user_input.lower() == "/bye":
            break
        print("\nAssistant>>", end=" ", flush=True)
        chatEngine.generate_response(user_input)


if __name__ == "__main__":
    chat_loop()