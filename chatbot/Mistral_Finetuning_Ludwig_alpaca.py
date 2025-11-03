from transformers import AutoTokenizer, PreTrainedModel

import os
import yaml
import logging
from ludwig.api import LudwigModel

# Hugging Face token
os.environment["HUGGING_FACE_HUB_TOKEN"] = os.getenv("HUGGINGFACE_API_KEY")

# Ludwig configuration
config_str = """
model_type: llm
base_model: mistralai/Mistral-7B-v0.1
quantization:
	bits: 4
adapter:
	type: lora
prompt:
	template: |
		### Instruction:
		{instruction}
		### Input:
		{input}
		### Response:
input_features:
	- name:	prompt
      type: text
      preprocessing:
			max_sequence_length: 256
output_features:
	- name: output
	  type: text
	  preprocessing:
	  max_sequence_length: 256
trainer:
	type: finetune
	learning_rate: 0.0001
	batch_size: 1
	gradient_accumulation_steps: 16
	epochs: 1
	learning_rate_scheduler:
		warmup_fraction: 0.01
preprocessing:
	sample_rate: 0.1
"""
config.yaml.safe_load(config_str)

# Train model
model = LudwigModel(config=config, logging_level= logging.INFO)
results = model.train(dataset="ludwig://alpaca")

# Save the model
model.save("Mistral-7B-v0.1-alpaca-trained")

