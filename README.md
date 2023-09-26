# StackExchange Bot
Through this project, we create a simple chatbot API by fine-tuning and training the OPT-1.3b model by applying reinforcement learning with human feedback (RLHF) on the StackExchange dataset and deploying it onto a remote backend server.

## Structure
### Server
The remote server backend resides in the `app/` directory. To run the server, use the `asgi.py` script:
```
python asgi.py
```
Before running the server, create an `llm/` directory in the same level with `app/` directory and place HuggingFace's pre-trained model into the directory together with the the tokenizer. To test the server, you can simply download the smaller version of the model from the HugginFace Hub: 
```
python -c "from transformers import AutoModelForCausalLM, AutoTokenizer;\
           AutoModelForCausalLM.from_pretrained('facebook/opt-125m', cache_dir='llm2');\
           AutoTokenizer.from_pretrained('facebook/opt-125m', cache_dir='llm2')"
```

### Client
We prepare a simple TUI to interact with the chatbot via the command line. To run the client, use the `cli.py` scripts:
```
python cli.py
```

### Training scripts
All the code for the training process resides in the `rlhf/` directory. Use the `training.ipynb` notebook to replicate the training process. Using sample implementation from the HuggingFace [*trl*](https://github.com/huggingface/trl) library and made some modifications/simplifications to the training process.
