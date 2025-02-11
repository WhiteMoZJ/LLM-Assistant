from ChatEngine.utils.chat_engine import ChatEngine
import os

def chat_loop():
    chatEngine = ChatEngine("http://localhost:8080/v1")
    '''
    llama.cpp: ChatEngine("http://localhost:8080/v1")
    LM Studio: ChatEngine("http://localhost:1234/v1")
    '''
    while True:
        user_input = input("\nYou >>").strip()
        if user_input.lower() == "/bye":
            break
        elif user_input == "":
            continue
        elif user_input.lower() == "/history":
            chatEngine.get_history()
            continue
        elif user_input.lower() == "/reset":
            chatEngine.reset_history()
            continue
        elif user_input.lower() == "/help" or user_input.lower() == "/":
            print("\nCommands:")
            print("/bye - Exit the chat")
            print("/history - Show chat history")
            print("/reset - Reset chat history")
            continue

        print("\nAssistant >>", end=" ", flush=True)
        chatEngine.generate_response(user_input)


if __name__ == "__main__":
    os.path.dirname(__file__)
    chat_loop()