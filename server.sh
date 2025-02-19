export MODEL="DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(cd $(dirname $0); pwd)/Server/llama.cpp
export OFFLOAD=32
export MAX_TOKENS=8192

# Start the server
# I put llama.cpp in Server folder
# replace the path with your own
Server/llama.cpp/llama-server --jinja --port 8080 -m Server/models/$MODEL -ngl $OFFLOAD -c $MAX_TOKENS