# -*- coding: utf-8 -*-
# import spacy
#
# # Load the pre-trained model
# nlp = spacy.load('en_core_web_sm')
#
# # Your text input
# text = ("This is a sentence mentioning a paper titled 'Attention Is All You Need' in the context.")
#
# # text = ("When Sebastian Thrun started working on self-driving cars at "
# #         "Google in 2007, few people outside of the company took him "
# #         "seriously. “I can tell you very senior CEOs of major American "
# #         "car companies would shake my hand and turn away because I wasn’t "
# #         "worth talking to,” said Thrun, in an interview with Recode earlier "
# #         "this week.")
# # Process the text
# doc = nlp(text)
#
# # Iterate over the entities and print them
# for ent in doc.ents:
#     print(ent.text, ent.label_)


# os.environ['OPENAI_API_KEY'] = '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'
#
# nlp = spacy.blank("en")
# config = {"task": {"@llm_tasks": "spacy.NER.v3", "labels": ["PERSON", "ORGANISATION"]}}
# llm = nlp.add_pipe("llm", config=config)
# nlp.initialize()
# doc = nlp("Jack and Jill rode up the hill in Harvard University.")
# print([(ent.text, ent.label_) for ent in doc.ents])

# from spacy_llm.util import assemble
#
# nlp = assemble("llm_config.cfg")
# doc = nlp("What are similar papers to Heterogeneous Graph Transformer by Bhandari Prakhar?")
# print([(ent.text, ent.label_) for ent in doc.ents])

import os
import torch

from accelerate import init_empty_weights, load_checkpoint_and_dispatch
from huggingface_hub import snapshot_download
from transformers import LlamaForCausalLM, LlamaTokenizer

LLM_PARAM: int = 13  # Choose from [7, 13, 70]
LLM_NAME: str = f"Llama-2-{LLM_PARAM}b-chat"
LLM_HF_PATH: str = f"meta-llama/{LLM_NAME}-hf"
CKPT_DIR = f"{os.getcwd()}/llama-weights-{LLM_PARAM}b"
if not os.path.exists(CKPT_DIR):
    os.system(f"mkdir {CKPT_DIR}")

tokenizer = LlamaTokenizer.from_pretrained(LLM_HF_PATH)
tokenizer.pad_token_id = tokenizer.eos_token_id

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# llama = LlamaForCausalLM.from_pretrained(
# 	pretrained_model_name_or_path=LLM_HF_PATH,
# 	torch_dtype=torch.bfloat16,
# 	)

# ckpt_path = snapshot_download(LLM_HF_PATH, local_dir=CKPT_DIR, ignore_patterns=["*.safetensors", "model.safetensors.index.json"]) # run this if you haven't downloaded the 70b model

# Load model
with init_empty_weights():
    model = LlamaForCausalLM.from_pretrained(CKPT_DIR)

model = load_checkpoint_and_dispatch(
	model,
	CKPT_DIR,
	device_map='auto',
	offload_folder=CKPT_DIR,
	offload_state_dict=True,
	dtype=torch.bfloat16,
	no_split_module_classes=["LlamaDecoderLayer"]
	)


print(tokenizer.decode(model.generate(**({ k: torch.unsqueeze(torch.tensor(v), 0) for k,v in tokenizer("Hi there, how are you doing?").items()}), max_new_tokens = 20).squeeze()))