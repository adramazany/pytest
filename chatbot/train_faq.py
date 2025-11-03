
import ollama

# Initialize the Ollama model
model = ollama.Model('llama3.2:latest')
ollama.embed()
ollama.embeddings()
ollama.


# Simple dataset
data = [
    {"input": "What is the capital of France?", "output": "The capital of France is Paris."},
    {"input": "What is the largest planet in our solar system?", "output": "The largest planet in our solar system is Jupiter."},
    {"input": "Who wrote 'To Kill a Mockingbird'?", "output": "Harper Lee wrote 'To Kill a Mockingbird'."},
    {"input": "Who is the president of USA?", "output": "Donald John Trump (born June 14, 1946) is an American politician, media personality, and businessman who is the 47th president of the United States. A member of the Republican Party, he served as the 45th president from 2017 to 2021."},
    {"input": "What is my name?", "output": "My name is Adel Ramezani."},
    {"input": "When it will be the next president election in USA?", "output": "The next presidential election in the United States is scheduled to take place on November 7, 2028."},
]

# Prepare the data for fine-tuning
train_data = [{"input": item["input"], "target": item["output"]} for item in data]

# Fine-tuning configuration
config = ollama.FineTuneConfig(
    epochs=3,
    batch_size=2,
    learning_rate=0.001
)

# Fine-tune the model
model.fine_tune(train_data, config)

# Save the fine-tuned model
model.save('fine_tuned_ollama_model')
