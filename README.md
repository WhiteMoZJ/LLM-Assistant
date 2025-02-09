# LLM-Assistant(Local test version)
## How to run
If you need online search function, set the api(*ChatEngine/utils/retriever.py*) and keys(*ChatEngine/config/key.json*)

- Python >= 3.10

### LM Studio
1. Install [LM Studio](https://lmstudio.ai/)
2. Run LM Studio server and load a model
3. set **ChatEngine/app.py** as
    ```python
    chatEngine = ChatEngine("http://localhost:1234/v1")
    ```

### llama.cpp - A pure-code version(WIP)
> Tools are unavailable
1. Install [llama.cpp](https://github.com/ggerganov/llama.cpp)
2. Put all llama.cpp libs and executable(*llama-server, llama.so, etc*) file in folder **Server/llama.cpp/**
3. run server.sh to start llama-server
    ```sh
    sh server.sh
    ```
    check the parameters to fit your device
4. set **ChatEngine/app.py** as
    ```python
    chatEngine = ChatEngine("http://localhost:8080/v1")
    ```
5. run **ChatEngine/app.py** to start chat

## Reference:
- [LM Studio](https://lmstudio.ai/)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [openai-python](https://github.com/openai/openai-python)
- [unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF](https://huggingface.co/unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF)