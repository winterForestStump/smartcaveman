Caveman version of Warren E. Buffett letters to shareholders. official letters source: [Berkshire Hathaway Inc. Website](https://www.berkshirehathaway.com/letters/letters.html)

link to gradio application

Setup: 
* [qwen-3-14b model](https://huggingface.co/unsloth/Qwen3-14B-unsloth-bnb-4bit) using unsloth to run on free google colab tier
* for txt document: text splitter CharacterTextSplitter from langchain library with separator="\n\n", chunk_size=1000, chunk_overlap=50. Model hyperparameters: MAX_NEW_TOKENS = 512, TEMPERATURE = 1.0, TOP_P = 0.95, TOP_K = 20
* for pdf document: PyMuPDFLoader for pdf document, chunked by page. model hyperparameters: MAX_NEW_TOKENS = 2056, TEMPERATURE = 1.0, TOP_P = 0.95, TOP_K = 20
* system_prompt: Respond terse like smart caveman. Drop all fluff. Use short words. Technical substance stay. Minimum tokens.



This application is created solely for educational and demonstrative purposes.