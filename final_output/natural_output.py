# -*- coding: utf-8 -*-
import re

import torch
from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer, set_seed

LLM_PARAM: int = 7
LLM_NAME: str = f"Llama-2-{LLM_PARAM}b-chat"
LLM_HF_PATH: str = f"meta-llama/{LLM_NAME}-hf"
MAX_LEN = 1000
TEMPERATURE = 0.9
TOP_P = 0.9
PADDING_TOKEN = "<pad>"
RESPONSE_SPLITTER = "Response:"
PROMPT_TEMPLATE = """
**User Query**: 
"{user_query}"

**Model Outputs**:
"{model_output}"

**Response Generation Instructions**:
- Use the user query to guide an conversational response that incorporates model outputs. 
- Omitting any complex metrics or data in the model output.
- Do not explain the title or the content of the paper.
- Use quotation marks for direct references to model outputs if you choose to include part of it in the response.
- Be informative, concise and clear in your response, ensuring relevance to the user query. 
"""
# Aim to inform and engage in a friendly manner, ensuring concision, clarity and relevance to the user query.
# - Please use quotation marks for direct references to model outputs if you choose to include part of its contents in your response.
# - Introduce the most relevant model output in a conversational tone.
# - Provide a concise explanation or summary that ties directly back to the user query, omitting any complex metrics or data.
# - Only consider textual contents in the model outputs. Do not include any metrics from the model outputs in your generated response.
# - Conclude with an offer for further assistance that encourages the user to engage more if needed.
REGEX_PATTERN = re.compile(
	r"<unk>|<pad>|<s>|</s>|\[PAD\]|<\|endoftext\|>|\[UNK\]|\[CLS\]|\[MASK\]|<\|startofpiece\|>|<\|endofpiece\|>|\[gMASK\]|\[sMASK\]"
	)

def set_llama_config(model, tokenizer, device) -> GenerationConfig:
	"""
	Set Llama configurations. Follow up HF tips https://huggingface.co/docs/transformers/model_doc/llama2

	:param model: LLM model
	:param tokenizer: LLM tokenizer
	:param device: PyTorch device
	:return: config for generating response
	"""

	pad_token_id = tokenizer.add_special_tokens({"pad_token": PADDING_TOKEN})
	model.resize_token_embeddings(len(tokenizer))
	model.config.pad_token_id = pad_token_id
	model.config.pretraining_tp = 100
	model.to(device)
	model.eval()

	gen_config = GenerationConfig(
		max_new_tokens=MAX_LEN,
		temperature=TEMPERATURE,
		top_p=TOP_P,
		do_sample=True,
		)
	return gen_config


def gen_natural_output(user_query: str, machine_output: str) -> str:
	"""
	Generates a natural language output based on the query and the output.

	:param user_query: The input user query.
	:param machine_output: The output of our model.
	:return: A natural language output in plain English.
	"""
	prompt = PROMPT_TEMPLATE.format(user_query=user_query, model_output=machine_output)
	input_text = f"{prompt}\n\n{RESPONSE_SPLITTER}"
	input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
	with torch.no_grad():
		output_ids = model.generate(input_ids, generation_config=gen_config)
	output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
	clean_output = output_text.split(RESPONSE_SPLITTER, 1)[-1].strip()
	clean_output = REGEX_PATTERN.sub("", clean_output.strip()).strip()
	return clean_output



if __name__ == "__main__":
	set_seed(42)
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	model = LlamaForCausalLM.from_pretrained(
		pretrained_model_name_or_path=LLM_HF_PATH,
		torch_dtype=torch.bfloat16,
		)
	tokenizer = LlamaTokenizer.from_pretrained(LLM_HF_PATH)
	gen_config = set_llama_config(model=model, tokenizer=tokenizer, device=device)

	ex_user_query = "Recommend me similar papers to the paper 'light incorporating a clip and bottle opener'."
	ex_machine_output = """
method and base station for reducing forward transmission power in cluster system :  0.50766593
two batteries mobile phone :  0.4924111
the importance of negative associations and the discovery of association rule pairs :  0.45861343
chemical investigation result computation and data processing software package :  0.43625128
automatic real time unsupervised spatio temporal 3d object detection using rgb d cameras :  0.43452704
printer and data transfer method :  0.43098667
integrated two way measuring force device of aircraft :  0.42745852
learning compositional koopman operators for model based control :  0.42705858
method and system for providing content service using multiple devices :  0.42486614
"""
	natural_output = gen_natural_output(user_query=ex_user_query, machine_output=ex_machine_output)
	print(natural_output)


